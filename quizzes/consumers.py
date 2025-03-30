import json
from time import sleep
from django.core.cache import cache
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Quiz, Question

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the quiz ID from the URL and create a group name
        self.quiz_id = self.scope['url_route']['kwargs']['quiz_id']
        self.group_name = f"quiz_{self.quiz_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Increment the user count in the cache and send the updated count to the group
        await self.change_user_count(1)
        user_count = await sync_to_async(cache.get)(f"{self.group_name}_count")
        print(f"The current user count is: {user_count}")
        await self.broadcast_user_count(user_count)


    async def disconnect(self, close_code):
        print(f"The close code was {close_code}")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.change_user_count(-1)
        user_count = await sync_to_async(cache.get)(f"{self.group_name}_count")
        await self.broadcast_user_count(user_count)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('action') == 'start_quiz':
            await self.send_next_question()
        elif data.get('action') == 'submit_answer':
            question_id = data.get('question_id')
            user_answer = data.get('answer_text')
            await self.process_answer(question_id, user_answer)
            # sleep 1s before sending the next question to allow the answer to be shown.
            sleep(1.0)
            await self.send_next_question()

    async def change_user_count(self, delta):
        key = f"{self.group_name}_count"
        count = cache.get(key, 0)
        count += delta
        cache.set(key, count)

    async def broadcast_user_count(self, user_count):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "quiz_user_count_update",
                "active_users": user_count,
            }
        )

        await self.channel_layer.group_send(
            "global_notification_group",
            {
                "type": "quiz_user_count_update",
                "quiz_id": self.quiz_id,
                "active_users": user_count,
            }
        )

    async def quiz_user_count_update(self, event):
        await self.send(
            text_data=json.dumps({
                "action": "user_count",
                "active_users": event["active_users"],
            })
        )


    async def send_next_question(self):
        quiz = await sync_to_async(Quiz.objects.get)(pk=self.quiz_id)
        questions = await sync_to_async(list)(
            quiz.question_set.all().order_by('id')
        )

        if not hasattr(self, 'current_q_idx'):
            self.current_q_idx = 0
        else:
            self.current_q_idx += 1

        if self.current_q_idx < len(questions):
            question = questions[self.current_q_idx]
            await self.send(text_data=json.dumps({
                "action": "next_question",
                "question_id": question.id,
                "question_text": question.question_text,
                "question_answers": question.answer_options,
                "time_limit": 10
            }))
        else:
            # Upon finishing the quiz, we increment the count 
            quiz.times_taken += 1

            # And check for the high score
            if self.score >= quiz.high_score:
                quiz.high_score = self.score

            # Saving changes to the quiz
            await sync_to_async(quiz.save)()

            await self.send(text_data=json.dumps({
                "action": "quiz_finished",
                "score": self.score,
                "message": "Quiz complete!"
            }))

    async def process_answer(self, question_id, user_answer):
        question = await sync_to_async(Question.objects.get)(pk=question_id)
        is_correct = (question.correct_answer_text.lower() == user_answer.lower())

        question.answered_times += 1
        if is_correct:
            question.correct_answered_times += 1

        if not hasattr(self, 'score'):
            self.score = 0
        if is_correct:
            self.score += 1

        await sync_to_async(question.save)()

        await self.send(text_data=json.dumps({
                "action": "answer_result",
                "is_correct": is_correct,
        }))


class GlobalNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "global_notification_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get("action") == "request_initial_counts":
            quiz_ids = data["quiz_ids"]

            for quiz_id in quiz_ids:
                quiz_users = await sync_to_async(cache.get)(f"quiz_{quiz_id}_count", 0)

                await self.send(text_data=json.dumps({
                    "quiz_id": quiz_id,
                    "active_users": quiz_users
                }))

    async def quiz_user_count_update(self, event):
        await self.send(text_data=json.dumps({
            "quiz_id": event["quiz_id"],
            "active_users": event["active_users"],
        }))