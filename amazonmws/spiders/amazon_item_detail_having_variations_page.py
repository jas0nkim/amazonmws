from os.path import basename

from amazonmws.spiders.amazon_item_detail_page import AmazonItemDetailPageSpider
from amazonmws.loggers import GrayLogger as logger


class AmazonItemDetailHavingVariationsPageSpider(AmazonItemDetailPageSpider):

    def __extra_conditions(self):
        no_size_variations = True

        size_variations_dropdown = False
        size_variations_buttons = False

        try:
            size_variations_dropdown = self.driver.find_element_by_css_selector('#variation_size_name #native_dropdown_selected_size_name')

        except NoSuchElementException:
            logger.exception('No size variations element')
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        try:
            size_variations_buttons = self.driver.find_element_by_css_selector('#variation_size_name ul')

        except NoSuchElementException:
            logger.exception('No size variations element')
        
        except StaleElementReferenceException, e:
            logger.exception(e)

        if size_variations_dropdown or size_variations_buttons:
            no_size_variations = False

        return no_size_variations
