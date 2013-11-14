# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Subdomain(models.Model):
    '''One atlas page'''
    # Status of page
    DISABLED = 0
    ACTIVE = 1
    ARCHIVED = 2

    SUBDOMAIN_STATUS = (
        (DISABLED, _('disabled')),
        (ACTIVE, _('active')))

    class Meta:
        ordering = ['order']
        verbose_name = _('map')
        verbose_name_plural = _('maps')

    url = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=50)
    isCurrent = models.BooleanField(db_column='is_current')
    status = models.SmallIntegerField(choices=SUBDOMAIN_STATUS)
    order = models.IntegerField()
    disclaimer = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    def name(self):
        return self.title

    def full_url(self):
        if self.url:
            return "%s.newrynda.org" % self.url
        else:
            return "newrynda.org"


class Category(models.Model):
    ''' Категория сообщения '''
    class Meta:
        ordering = ['order']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    name = models.CharField(
        max_length=200, db_column='name',
        verbose_name=_('name'))
    description = models.TextField(
        blank=True, db_column='description',
        verbose_name=_('description'))
    color = models.CharField(
        max_length=7, db_column='color',
        default='#000000', verbose_name=_('color'))
    slug = models.SlugField(
        max_length=255, db_column='slug',
        verbose_name=_('slug'), blank=True)
    icon = models.CharField(
        max_length=255, null=True, blank=True,
        db_column='icon', verbose_name=_('icon'))
    order = models.SmallIntegerField(db_column='order')
    subdomain = models.ForeignKey(
        Subdomain, null=True, blank=True,
        db_column='subdomain_id', verbose_name=_('subdomain'))
    group = models.ForeignKey("CategoryGroup", null=True, blank=True)

    def __unicode__(self):
        return self.name

    def unlink(self):
        '''Remove link to category group'''
        self.group = None
        self.save()


class CategoryGroup(models.Model):
    '''Grouping categories. One category must be in one group.'''
    class Meta:
        ordering = ['order']
        verbose_name = _('category group')
        verbose_name_plural = _('category groups')

    name = models.CharField(
        max_length=200,
        verbose_name=_('category group name'))
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    def add_category(self, category):
        '''Add category to group '''
        category.group = self
        category.save()


class Infopage(models.Model):
    class Meta:
        pass

    title = models.CharField(
        max_length=255, db_column='title',
        verbose_name=_('title'))
    text = models.TextField(db_column='text', verbose_name=_('text'))
    active = models.BooleanField(default=False, verbose_name=_('is active'))
    slug = models.SlugField(max_length=255, verbose_name=_('slug'))
    default = models.BooleanField(
        default=False, verbose_name=_('default page'))

    def __unicode__(self):
        return self.title
