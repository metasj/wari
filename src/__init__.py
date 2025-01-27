# import logging
# from typing import Optional
#
# from wikibaseintegrator import wbi_config  # type: ignore
# from wikibaseintegrator.wbi_helpers import execute_sparql_query  # type: ignore
#
# import config
# from src.helpers.console import console
# from src.models.wikimedia.enums import WikimediaDomain
# from src.models.wikimedia.wikipedia.article import WikipediaArticle
# from src.wcd_base_model import WcdBaseModel
#
# logging.basicConfig(level=config.loglevel)
# logger = logging.getLogger(__name__)
#
#
# class WcdImportBot(WcdBaseModel):
#     """This class controls the import bot
#
#     The language code is the one used by Wikimedia Foundation"""
#
#     language_code: str = "en"
#     event_max_count: int = 0  # 0 means deprecated, ie. no maximum ie. run forever
#     page_title: Optional[str]
#     percent_references_hashed_in_total: Optional[int]
#     # wikibase: Wikibase = IASandboxWikibase()
#     wikimedia_site: WikimediaDomain = WikimediaDomain.wikipedia
#     # wikidata_qid: str = ""
#     testing: bool = False
#     wikipedia_article: Optional[WikipediaArticle] = None
#
#     def __flush_cache__(self):
#         # We deprecate flushing the cache, since we will lose the last
#         #  update information if doing so, and we cannot currently populate
#         #  it with a query because the timestamp is not uploaded to wikibase
#         raise DeprecationWarning("This has been deprecated since 2.1.0-alpha3.")
#         # self.__setup_cache__()
#         # self.cache.flush_database()
#
#     # def __gather_and_print_statistics__(self):
#     #     console.print(self.wikibase.title)
#     #     wcr = WikibaseCrudRead(wikibase=self.wikibase)
#     #     console.print(f"Number of pages: {wcr.number_of_pages}")
#     #     console.print(f"Number of references: {wcr.number_of_references}")
#     #     console.print(f"Number of websites: {wcr.number_of_website_items}")
#     #     attributes = [a for a in dir(self.wikibase)]
#     #     for attribute in attributes:
#     #         if attribute in {**wcd_externalid_properties, **wcd_string_properties}:
#     #             value = wcr.get_external_identifier_statistic(
#     #                 wikibase_property_id=getattr(self.wikibase, attribute)
#     #             )
#     #             console.print(f"Number of {attribute}: {value}")
#
#     # def __rebuild_cache__(self):
#     #     """Rebuild the cache"""
#     #     # We don't flush first since 2.1.0-alpha3
#     #     self.__setup_cache__()
#     #     if self.cache:
#     #         wcrsandbox = WikibaseCrudRead(wikibase=IASandboxWikibase())
#     #         data = wcrsandbox.__get_all_items_and_hashes__()
#     #         logger.info("Rebuilding the sandbox cache")
#     #         count_sandbox = 1
#     #         for entry in data:
#     #             self.__log_to_file__(message=str(entry), file_name="cache-content.log")
#     #             hash_value = entry[1]
#     #             wcdqid = entry[0]
#     #             logger.debug(f"Inserting {hash_value}:{wcdqid} into the cache")
#     #             self.cache.ssdb.set_value(key=hash_value, value=wcdqid)
#     #             count_sandbox += 1
#     #         wcrswc = WikibaseCrudRead(wikibase=WikiCitationsWikibase())
#     #         data = wcrswc.__get_all_items_and_hashes__()
#     #         logger.info("Rebuilding the wikicitations cache")
#     #         count_wikicitations = 1
#     #         for entry in data:
#     #             self.__log_to_file__(message=str(entry), file_name="cache-content.log")
#     #             hash_value = entry[1]
#     #             wcdqid = entry[0]
#     #             # logger.debug(f"Inserting {hash_value}:{wcdqid} into the cache")
#     #             self.cache.ssdb.set_value(key=hash_value, value=wcdqid)
#     #             count_wikicitations += 1
#     #         console.print(
#     #             f"Inserted a total of {count_sandbox+count_wikicitations} "
#     #             f"entries into the cache"
#     #         )
#     #     else:
#     #         raise RuntimeError("self.cache could not be set up.")
#
#     # @staticmethod
#     # def __setup_argparse_and_return_args__():
#     #     #  add possibility to specify the wikipedia language version to work on
#     #     parser = argparse.ArgumentParser(
#     #         formatter_class=argparse.RawDescriptionHelpFormatter,
#     #         description="""
#     # WCD Import Bot imports references and pages from Wikipedia
#     #
#     # Example adding one page:
#     # '$ ./wcdimportbot.py --import-title "Easter Island"'
#     #
#     # Example looking up a md5hash:
#     # '$ ./wcdimportbot.py --lookup-md5hash e98adc5b05cb993cd0c884a28098096c'
#     #
#     # Example importing 5 pages (any page on the Wiki):
#     # '$ ./wcdimportbot.py --max-range 5'
#     #
#     # Example importing 5 pages from a specific category title (recursively):
#     # '$ ./wcdimportbot.py --max-range 5 --category "World War II"'
#     #
#     # Example importing all pages from a specific category title (recursively):
#     # '$ ./wcdimportbot.py --category "World War II"'
#     #
#     # Example rebuild the caches of all supported Wikibase instances:
#     # '$ ./wcdimportbot.py --rebuild-cache'""",
#     #     )
#     #     parser.add_argument(
#     #         "-c",
#     #         "--category",
#     #         help="Import range of pages from a specific category title recursively",
#     #     )
#     #     # DEPRECATED since 2.1.0-alpha2
#     #     # parser.add_argument(
#     #     #     "-d",
#     #     #     "--delete-page",
#     #     #     help=(
#     #     #         "Delete a single page from WikiCitations and the cache by title "
#     #     #         "(Defaults to English Wikipedia for now). "
#     #     #         "Note: This does not delete the reference items associated "
#     #     #         "with the page."
#     #     #     ),
#     #     # )
#     #     parser.add_argument(
#     #         "-r",
#     #         "--max-range",
#     #         help="Import max range of pages via http",
#     #     ),
#     #     # DEPRECATED since 2.1.0-alpha2
#     #     # parser.add_argument(
#     #     #     "--flush-cache",
#     #     #     action="store_true",
#     #     #     help="Remove all items from the cache",
#     #     # ),
#     #     parser.add_argument(
#     #         "-i",
#     #         "--import-title",
#     #         help=(
#     #             "Title to import from a Wikipedia (Defaults to English Wikipedia for now) via http"
#     #         ),
#     #     )
#     #     parser.add_argument(
#     #         "-l",
#     #         "--lookup-md5hash",
#     #         help=(
#     #             "Lookup md5hash in the cache (if enabled) "
#     #             "and WikiCitations via SPARQL (used mainly for debugging)"
#     #         ),
#     #     )
#     #     # DEPRECATED since 2.1.0-alpha2
#     #     # parser.add_argument(
#     #     #     "--rinse",
#     #     #     action="store_true",
#     #     #     help="Rinse all page and reference items and delete the cache",
#     #     # )
#     #     parser.add_argument(
#     #         "-s",
#     #         "--statistics",
#     #         action="store_true",
#     #         help="Show statistics about the supported Wikibase instances",
#     #     )
#     #     parser.add_argument(
#     #         "-wc",
#     #         "--wikicitations",
#     #         action="store_true",
#     #         #  revert to defaulting to Wikicitaitons again
#     #         help="Work against Wikicitations. The bot defaults to IASandboxWikibase.",
#     #     )
#     #     return parser.parse_args()
#
#     # def __setup_wikibase_integrator_configuration__(
#     #     self,
#     # ) -> None:
#     #     wbi_config.config["USER_AGENT"] = "wcdimportbot"
#     #     # wbi_config.config["WIKIBASE_URL"] = self.wikibase.wikibase_url
#     #     # wbi_config.config["MEDIAWIKI_API_URL"] = self.wikibase.mediawiki_api_url
#     #     # wbi_config.config["MEDIAWIKI_INDEX_URL"] = self.wikibase.mediawiki_index_url
#     #     # wbi_config.config["SPARQL_ENDPOINT_URL"] = self.wikibase.sparql_endpoint_url
#
#     # @validate_arguments
#     # def delete_one_page(self):  # , title: str
#     #     """Deletes one page from the Wikibase and from the cache"""
#     #     raise DeprecationWarning("This has been deprecated since 2.1.0-alpha2.")
#     #     # logger.debug("delete_one_page: running")
#     #     # with console.status(f"Deleting {title}"):
#     #     #     from src.models.wikimedia.wikipedia.article import (
#     #     #         WikipediaArticle,
#     #     #     )
#     #     #
#     #     #     page = WikipediaArticle(
#     #     #         wikibase=self.wikibase,
#     #     #         language_code=self.language_code,
#     #     #         wikimedia_site=self.wikimedia_site,
#     #     #     )
#     #     #     page.__get_wikipedia_article_from_title__(title=title)
#     #     #     page.__generate_hash__()
#     #     #     # delete from WCD
#     #     #     cache = Cache()
#     #     #     cache.connect()
#     #     #     cache_return = cache.check_page_and_get_wikibase_qid(wikipedia_article=page)
#     #     #     if cache_return.item_qid:
#     #     #         logger.debug(
#     #     #             f"Found {cache_return.item_qid} and trying to delete it now"
#     #     #         )
#     #     #         wc = WikibaseCrudDelete(wikibase=self.wikibase)
#     #     #         result = wc.__delete_item__(item_id=cache_return.item_qid)
#     #     #         if result == Result.SUCCESSFUL:
#     #     #             if page.md5hash is not None:
#     #     #                 cache.delete_key(key=page.md5hash)
#     #     #                 logger.info(f"Deleted {title} from the cache")
#     #     #                 console.print(
#     #     #                     f"Deleted {title} from {self.wikibase.__repr_name__()}"
#     #     #                 )
#     #     #                 return result
#     #     #             else:
#     #     #                 raise ValueError("md5hash was None")
#     #     #         else:
#     #     #             raise WikibaseError("Could not delete the page")
#     #     #     else:
#     #     #         logger.error("Got no item id from the cache")
#     #     #         return Result.FAILED
#
#     # @validate_arguments
#     # def get_and_extract_page_and_upload_by_title(self):
#     #     """Download and extract the page and the references
#     #     and then upload it to Wikibase. If the page is already
#     #     present in the Wikibase then compare it and all its
#     #     references to make sure we the data is reflecting changes
#     #     made in Wikipedia"""
#     #     # self.__setup_cache__()
#     #     if not self.page_title:
#     #         raise MissingInformationError("self.page_title was None")
#     #     from src.models.wikimedia.wikipedia.article import WikipediaArticle
#     #
#     #     self.wikipedia_article = WikipediaArticle(
#     #         wikibase=self.wikibase,
#     #         language_code=self.language_code,
#     #         wikimedia_site=self.wikimedia_site,
#     #         title=self.page_title,
#     #         # cache=self.cache,
#     #     )
#     #     self.wikipedia_article.__get_wikipedia_article_from_title__()
#     #     if self.wikipedia_article.found_in_wikipedia:
#     #         self.wikipedia_article.extract_and_parse_and_upload_missing_items_to_wikibase()
#     #
#     # @validate_arguments
#     # def get_and_extract_pages_by_range_via_http(
#     #     self, max_count: int = None, category_title: str = None
#     # ) -> None:
#     #     """
#     #     This method gets all pages in the main namespace up to max_count
#     #     It uses pywikibot
#     #     """
#     #     # self.__setup_cache__()
#     #     from pywikibot import Category, Site  # type: ignore
#     #
#     #     from src.models.wikimedia.wikipedia.article import WikipediaArticle
#     #
#     #     if max_count is not None:
#     #         logger.debug(f"Setting max_count to {max_count}")
#     #         self.event_max_count = int(max_count)
#     #     count: int = 0
#     #     # https://stackoverflow.com/questions/59605802/
#     #     # use-pywikibot-to-download-complete-list-of-pages-from-a-mediawiki-server-without
#     #     site = Site(code=self.language_code, fam=str(self.wikimedia_site.value))
#     #     if category_title:
#     #         category_page = Category(title=category_title, source=site)
#     #         for page in category_page.articles(recurse=True):
#     #             if self.event_max_count and count >= self.event_max_count:
#     #                 logger.debug("breaking now")
#     #                 break
#     #             # page: Page = page
#     #             #  and isinstance(page, Page)
#     #             if not page.isRedirectPage():
#     #                 count += 1
#     #                 # console.print(count)
#     #                 logger.info(
#     #                     f"{page.pageid} {page.title()} Redirect:{page.isRedirectPage()}"
#     #                 )
#     #                 # raise DebugExit()
#     #                 wikipedia_article = WikipediaArticle(
#     #                     wikibase=self.wikibase,
#     #                     language_code=self.language_code,
#     #                     latest_revision_date=page.editTime(),
#     #                     latest_revision_id=page.latest_revision_id,
#     #                     page_id=page.pageid,
#     #                     title=str(page.title()),
#     #                     wikimedia_site=self.wikimedia_site,
#     #                     wikitext=page.text,
#     #                     cache=self.cache,
#     #                 )
#     #                 wikipedia_article.extract_and_parse_and_upload_missing_items_to_wikibase()
#     #     else:
#     #         for page in site.allpages(namespace=0):
#     #             if count >= self.event_max_count:
#     #                 break
#     #             from pywikibot import Page
#     #
#     #             page: Page = page  # type: ignore
#     #             if not page.isRedirectPage():
#     #                 count += 1
#     #                 # console.print(count)
#     #                 logger.info(f"{page.pageid} {page.title()}")
#     #                 # raise DebugExit()
#     #                 wikipedia_article = WikipediaArticle(
#     #                     language_code=self.language_code,
#     #                     latest_revision_date=page.editTime(),
#     #                     latest_revision_id=page.latest_revision_id,
#     #                     page_id=page.pageid,
#     #                     title=str(page.title()),
#     #                     wikimedia_site=self.wikimedia_site,
#     #                     wikitext=page.text,
#     #                     wikibase=self.wikibase,
#     #                     cache=self.cache,
#     #                 )
#     #                 wikipedia_article.extract_and_parse_and_upload_missing_items_to_wikibase()
#
#     # def print_statistics(self):
#     #     self.__calculate_statistics__()
#     #     logger.info(
#     #         f"A total of {self.total_number_of_references} references "
#     #         f"has been processed and {self.total_number_of_hashed_references} "
#     #         f"({self.percent_references_hashed_in_total}%) could be hashed on "
#     #         f"a total of {len(self.pages)} pages."
#     #     )
#
#     # @staticmethod
#     # def rinse_all_items_and_cache():
#     #     """Delete all page and reference items and clear the SSDB cache"""
#     #     raise DeprecationWarning("This has been deprecated since 2.1.0-alpha2.")
#     #     # wc = WikibaseCrudDelete(wikibase=self.wikibase)
#     #     # wc.delete_imported_items()
#     #     # self.__flush_cache__()
#
#     @staticmethod
#     def run():
#         """This method handles running the bot
#         based on the given command line arguments."""
#         raise DeprecationWarning("We no longer support running the bot")
#         # self.__setup_cache__()
#         # args = self.__setup_argparse_and_return_args__()
#         # if args.wikicitations:
#         #     self.wikibase = WikiCitationsWikibase()
#         # DEPRECATED since 2.1.0-alpha2
#         # if args.rinse:
#         #     self.rinse_all_items_and_cache()
#         # elif args.rebuild_cache:
#         #     self.__rebuild_cache__()
#         # elif args.flush_cache:
#         #     self.__flush_cache__()
#         # elif args.import_title:
#         #     logger.info(f"importing title {args.import_title}")
#         #     self.page_title = args.import_title
#         #     self.get_and_extract_page_and_upload_by_title()
#         # DEPRECATED since 2.1.0-alpha2
#         # elif args.delete_page:
#         #     logger.info("deleting page")
#         #     self.delete_one_page(title=args.delete_page)
#         # elif args.max_range or args.category:
#         #     logger.info("Importing range of pages")
#         #     self.get_and_extract_pages_by_range_via_http(
#         #         max_count=args.max_range, category_title=args.category
#         #     )
#         # elif args.statistics:
#         #     bot = WcdImportBot(wikibase=IASandboxWikibase())
#         #     bot.__gather_and_print_statistics__()
#         #     # DISABLED because it returns 503 now.
#         #     bot = WcdImportBot(wikibase=WikiCitationsWikibase())
#         #     bot.__gather_and_print_statistics__()
#         # else:
#         #     console.print("Got no arguments. Try 'python wcdimportbot.py -h' for help")
#
#     # def get_and_extract_page_by_wdqid(self):
#     #     raise DeprecationWarning("deprecated because of failed test since 2.1.0-alpha2")
#     #     # from src.models.wikimedia.wikipedia.article import WikipediaArticle
#     #     #
#     #     # page = WikipediaArticle(
#     #     #     wikibase=self.wikibase,
#     #     #     language_code=self.language_code,
#     #     #     wikimedia_site=self.wikimedia_site,
#     #     #     wdqid=self.wikidata_qid,
#     #     # )
#     #     # page.__get_wikipedia_article_from_wdqid__()
#     #     # page.extract_and_parse_and_upload_missing_items_to_wikibase()
