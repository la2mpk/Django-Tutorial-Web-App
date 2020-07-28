import datetime
import random

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, days, choices=('choice 1',)):
    """
    Create a question with 'question_text' and published the given number of 'days' offset to now
    (negative for questions published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    for choice in choices:
        question.choice_set.create(choice_text=choice)
    return question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for question whose pub_date is in the Future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recenlty() returns False for question whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() return True for question whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class IndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questiosn exist, an appropiate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay encuestas disponibles')
        self.assertQuerysetEqual(response.context['latest_questions_list'], [])

    def test_question_with_out_choices(self):
        """
        Question with out choices are not displayed on the index page.
        """
        create_question(question_text='Question with out choices', days=0, choices=[])
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_questions_list'], [])

    def test_question_with_choices(self):
        """
        Question with choices are displayed on the index page.
        """
        create_question(question_text='Question with choices', days=0)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_questions_list'], ['<Question: Question with choices>'])

    def test_past_question(self):
        """
        Question with a pub_date in the past are displayed on the index page.
        """
        create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_questions_list'], ['<Question: Past Question>'])

    def test_future_question(self):
        """
        Question with a pub_date in the future are not displayed on the index page.
        """
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_questions_list'], [])

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text='Past question 1', days=-30)
        create_question(question_text='Past question 2', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_questions_list'], ['<Question: Past question 2>',
                                                                             '<Question: Past question 1>'])


class DetailViewTests(TestCase):

    def test_question_with_out_choices(self):
        """
        Question with out choices are not displayed on the index page.
        """
        question = create_question(question_text='Question with out choices', days=0, choices=[])
        response = self.client.get(reverse('polls:details', args=(question.id, )))
        self.assertEqual(response.status_code, 404)

    def test_question_with_choices(self):
        """
        Question with choices are displayed on the index page.
        """
        question = create_question(question_text='Question with choices', days=0)
        response = self.client.get(reverse('polls:details', args=(question.id, )))
        self.assertContains(response, question.question_text)

    def test_future_question(self):
        """
        The details view of a question with a pub_date in the future returns a 404 not found.
        """
        future_question = create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:details', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The details view of a question with a pub_date in the past displays the question's text.
        """
        past_question = create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:details', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)


class ResultsViewTests(TestCase):

    def test_question_with_out_choices(self):
        """
        Question with out choices are not displayed on the index page.
        """
        question = create_question(question_text='Question with out choices', days=0, choices=[])
        response = self.client.get(reverse('polls:results', args=(question.id, )))
        self.assertEqual(response.status_code, 404)

    def test_question_with_choices(self):
        """
        Question with choices are displayed on the index page.
        """
        question = create_question(question_text='Question with choices', days=0)
        response = self.client.get(reverse('polls:results', args=(question.id, )))
        self.assertContains(response, question.question_text)

    def test_future_question(self):
        """
        The results view of a quesion with a pub_date in the future returns a 404 not found.
        """
        future_question = create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:results', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The results view of a quesion with a pub_date in the past displays the question's text.
        """
        past_question = create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:results', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)
