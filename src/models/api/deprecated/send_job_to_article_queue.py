# import logging
#
# from pydantic import BaseModel
#
# import config
# from src.models.wikibase import Wikibase
#
# from src.models.wikibase.wikicitations_wikibase import WikiCitationsWikibase
#
# logger = logging.getLogger(__name__)
#
#
# class SendJobToArticleQueue(BaseModel):
#     message: Message
#     testing: bool = False
#
#     def publish_to_article_queue(self) -> bool:
#         logger.debug("publish_to_article_queue: Running")
#         logger.info(f"Publishing message with {self.message.dict()}")
#         if not self.testing:
#             if config.use_sandbox_wikibase_backend_for_wikicitations_api:
#                 wikibase: Wikibase = IASandboxWikibase()
#             else:
#                 wikibase = WikiCitationsWikibase()
#             work_queue = WorkQueue(wikibase=wikibase)
#             return work_queue.publish(message=self.message)
#         else:
#             return False
