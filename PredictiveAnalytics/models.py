from django.db import models

# Create your models here.

class Vissight_Phrase(models.Model):
    name: models.CharField(max_length=60)
    value:models.FloatField

    def get_vissight_phrase_name(self):
        return self.name

    def get_vissight_phrase_value(self):
        return self.value




class Vissight_Word(models.Model):
    name: models.CharField(max_length=60)
    value:models.FloatField

    def get_vissight_word_name(self):
        return self.name

    def get_vissigt_word_value(self):
        return self.value




# class Vissight_Topic (models.Model):
#     phrase: models.ForeignKey(Vissight_Phrase)
#     word: models.ForeignKey(Vissight_Word)
#
#     def get_vissight_topic_phrases(self):
#         return self.phrase
#
#     def get_vissigt_topic_words(self):
#         return self.word



class Vissight_Dictionary(models.Model):
    date:models.IntegerField
    value: models.IntegerField

    def get_vissight_topicstat_date(self):
        return self.date

    def get_vissigt_topicstat_value(self):
        return self.value



# class Vissight_Data (models.Model):
#     topic: models.ForeignKey(Vissight_Topic)
#     topicstat: models.ForeignKey(Vissight_Topicstat)
#
#     def get_vissight_topics(self):
#         return self.topic
#
#     def get_vissigt_topicstats(self):
#         return self.topicstat



class Datapoint_Visualization (models.Model):
    date: models.DateField
    value: models.IntegerField

    def get_datapoint_date(self):
        return self.date

    def get_datapoint_value(self):
        return self.value