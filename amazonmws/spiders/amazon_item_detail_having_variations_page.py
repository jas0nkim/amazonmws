from amazonmws.spiders.amazon_item_detail_page import AmazonItemDetailPageSpider

class AmazonItemDetailHavingVariationsPageSpider(AmazonItemDetailPageSpider):

    def __extra_conditions(self):
        no_size_variations = True

        size_variations_dropdown = False

        try:
            size_variations_dropdown = self.driver.find_element_by_css_selector('#variation_size_name #native_dropdown_selected_size_name')

        except NoSuchElementException as err:
            print 'No size variations element:', err
        
        except StaleElementReferenceException as err:
            print 'Element is no longer attached to the DOM:', err

        if size_variations_dropdown:
            no_size_variations = False

        return no_size_variations
