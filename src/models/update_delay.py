from datetime import datetime, timedelta
from typing import Any, Optional

import config
from src.models.cache import Cache
from src.models.hash_ import Hash_
from src.wcd_base_model import WcdBaseModel


class UpdateDelay(WcdBaseModel):
    """This class accepts a message or reference and
    helps determine if the update delay has passed or not"""

    cache: Cache = Cache()
    object_: Any
    time_of_last_update: Optional[datetime]

    @property
    def time_to_update(self) -> bool:
        self.cache.connect()
        from src.models.message import Message
        if isinstance(self.object_, Message):
            hash_ = Hash_(
                wikibase=self.object_.wikibase,
                language_code=self.object_.language_code,
                article_wikidata_qid=self.object_.article_wikidata_qid,
                title=self.object_.title,
                wikimedia_site=self.object_.wikimedia_site,
            )
        else:
            from src.models.wikimedia.wikipedia.reference import WikipediaReference
            if not isinstance(self.object_, WikipediaReference):
                raise ValueError("did not get Message or WikipediaReference")
            # Got reference
            hash_ = Hash_(
                wikibase=self.object_.wikibase,
                language_code=self.object_.language_code,
                title=self.object_.title,
                wikimedia_site=self.object_.wikimedia_site,
            )
        timestamp_string = self.cache.lookup_title_or_wdqid_last_updated(
            key=hash_.__entity_updated_hash__()
        )
        self.time_of_last_update = datetime.fromtimestamp(timestamp_string)
        return self.__delay_time_has_passed__()

    def __delay_time_has_passed__(self) -> bool:
        """We return true if the delay has passed and False otherwise"""
        if self.time_of_last_update:
            return self.time_of_last_update < (
                datetime.now() - timedelta(hours=config.article_update_delay_in_hours)
            )
        else:
            raise ValueError("self.time_of_last_update was None")
