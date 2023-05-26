from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['account', 'transfer', 'index', 'aboutus', 'mission',
                'career',
                'expectation',
                'contactus',
                'p_checking',
                'p_savings',
                'p_cards',
                'p_invest',
                'p_retire',
                'p_mortgage',
                'p_auto',
                'b_checking',
                'b_cash',
                'b_credit',
                'b_foreign',
                'b_wire',
                'c_solutions',
                'c_deals',
                'c_expertise',
                'i_outlook',
                'i_phil',
                'i_solutions', ]

    def location(self, item):
        return reverse(item)
