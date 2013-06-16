# -*- coding: utf-8 -*-
from django.db import models
import datetime

from PIL import Image
from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from tickets.func import rand_16

class Category(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField()
    sort=models.IntegerField()
    def __unicode__(self): return self.name

class Show(models.Model):
    name=models.CharField(max_length=30)
    location=models.CharField(max_length=30, default='Theatre')
    description = models.TextField()
    long_description = models.TextField(blank=True)
    poster=models.ImageField(upload_to='posters', blank=True, null=True)
    poster_wall=models.ImageField(upload_to='posters', blank=True, null=True)
    poster_page=models.ImageField(upload_to='posters', blank=True, null=True)
    poster_tiny=models.ImageField(upload_to='posters', blank=True, null=True)

    start_date=models.DateField(blank=True,null=True)  # these fields autoset from occurrences
    end_date=models.DateField(blank=True,null=True)


    category=models.ForeignKey('Category')

    IMAGE_SIZES = {'poster_wall'    : (126, 178),
                   'poster_page'    : (256, 362),       
                   'poster_tiny'    : (50, 71) }
    
    def is_current(self):
        today=datetime.date.today()
        if today>self.end_date: return False
        else: return True
    def sold_out(self):
        if self.occurrence_set.count() > 0:
            for occ in self.occurrence_set.all():
                if occ.sold_out()==False:
                    return False
            return True
        else:
            return False


    def gen_thumbs(self):
        img = Image.open(self.poster.path)
        #Convert to RGB
        if img.mode not in ('L', 'RGB'):
            img = img.convert('RGB')
        for field_name, size in self.IMAGE_SIZES.iteritems():
            print field_name
            field = getattr(self, field_name)
            working = img.copy()
            working.thumbnail(size, Image.ANTIALIAS)
            fp = StringIO()
            working.save(fp, "JPEG", quality=95)
            cf = InMemoryUploadedFile(fp, None, self.poster.name, 'image/jpeg',
                                  fp.len, None)
            field.save(name=self.poster.name+"_"+field_name, content=cf, save=True)
    def update_dates(self):
        if self.occurrence_set.count() > 0:
            first_show_date=self.occurrence_set.order_by('date')[0].date
            last_show_date=self.occurrence_set.order_by('-date')[0].date
            self.start_date=first_show_date
            self.end_date=last_show_date


    def save(self, *args, **kwargs):
        orig=Show.objects.get(pk=self.pk)
        self.update_dates()
        super(Show, self).save(*args, **kwargs)
        if not self.poster_wall and not self.poster_page and not self.poster_tiny:
            self.gen_thumbs()
        if self.poster!=orig.poster:
            self.gen_thumbs()
    
    def __unicode__(self):
        return self.name;

class OccurrenceManager(models.Manager):
    def get_avaliable(self,show):
        today=datetime.date.today()
        occs=Occurrence.objects.filter(show=show).filter(date__gt=today).all()
        ret=[]
        for oc in occs:
            if oc.sold_out(): pass
            else:
                ret.append((oc.id,oc.datetime_formatted()))
        print ret
        return ret

class Occurrence(models.Model):
    show=models.ForeignKey(Show)
    date=models.DateField()
    time=models.TimeField()
    maximum_sell=models.PositiveIntegerField()
    hours_til_close=models.IntegerField(default=3)

    objects=OccurrenceManager()

    def day_formatted(self):
        return self.date.strftime('%A')
    def time_formatted(self):
        return self.time.strftime('%-I%p').lower()
    def datetime_formatted(self):
        return self.date.strftime('%A %d %B ')+self.time.strftime('%-I%p').lower()

    def tickets_sold(self):
        tickets=Ticket.objects.filter(occurrence=self).filter(cancelled=False)
        sold=0
        for ticket in tickets:
            sold+=ticket.quantity
        return sold
    def sold_out(self):
        if self.tickets_sold()>=self.maximum_sell:
            return True
        else: return False

    def save(self, *args, **kwargs):
        super(Occurrence, self).save(*args, **kwargs)
        self.show.save()
    def __unicode__(self):
        return self.show.name+" on "+str(self.date)+" at "+str(self.time)

class Ticket(models.Model): 
    occurrence=models.ForeignKey(Occurrence)
    stamp=models.DateTimeField(auto_now=True)
    person_name=models.CharField(max_length=80)
    email_address=models.EmailField(max_length=80)
    quantity=models.IntegerField(default=1)
    cancelled=models.BooleanField(default=False)
    unique_code=models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code=""
        super(Occurrence, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.occurrence.show.name+" on "+str(self.occurrence.date)+" at "+str(self.occurrence.time)+" for "+self.person_name

