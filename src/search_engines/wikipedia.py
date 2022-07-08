import logging
logger = logging.getLogger(__name__)

import wikipediaapi

class Wikipedia:
    def __init__(self) -> None:
        self.wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)

    def page_search(self, text: str) -> str:
        """
        """
        logger.debug("> Searching for page '%s' ..." % text)
        result = self.wiki.page(text)

        if self.__exist__(page=result):
            if result.summary[-9:] == "refer to:":
                suggestions = self.__uncertain__(result)

                return suggestions
            else:
                return result.summary

    def __exist__(self, page) -> bool:
        """
        """
        logger.debug("> Checking if page exists ...")
        if page.exists():
            logger.info("[+] Page exists.")
            return True
        else:
            logger.error("[x] Page not found.")
            return False

    def __uncertain__(self, page) -> str:
        """
        """
        suggestions = page.text.split("\n\n")
        result = ""
        limit = 2
        for index, section in zip(range(limit), suggestions):
            logger.info("[+] %d suggestions" % index)

            logger.debug("> Appending %d of %d suggestions ..." % (index+1, len(suggestions)))
            result += "%s\n" % section
        
        result += "The search is too broad. Please be more precise."
        return result

