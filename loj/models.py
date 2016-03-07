from django.db import models


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return "question_text = {}, pub_date = {}".format(self.question_text, self.pub_date)

    class Meta:
        db_table = "db_question"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return "choice_text = {}, votes = {}".format(self.choice_text, self.votes)

    class Meta:
        db_table = "db_choice"
