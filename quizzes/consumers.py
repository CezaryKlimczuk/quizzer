import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Quiz, Question

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.quiz_id = self.scope['url_route']['kwargs']['quiz_id']
        self.group_name = f"quiz_{self.quiz_id}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('action') == 'start_quiz':
            await self.send_next_question()
        elif data.get('action') == 'submit_answer':
            question_id = data.get('question_id')
            user_answer = data.get('answer_text')
            await self.process_answer(question_id, user_answer)
            await self.send_next_question()

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
                "time_limit": 10
            }))
        else:
            await self.send(text_data=json.dumps({
                "action": "quiz_finished",
                "score": self.score,
                "message": "Quiz complete!"
            }))

    async def process_answer(self, question_id, user_answer):
        question = await sync_to_async(Question.objects.get)(pk=question_id)
        is_correct = (question.ansewer_text.lower() == user_answer.lower())

        question.answered_times += 1
        if is_correct:
            question.correct_answered_times += 1

        if not hasattr(self, 'score'):
            self.score = 0
        if is_correct:
            self.score += 1

        await sync_to_async(question.save)()
