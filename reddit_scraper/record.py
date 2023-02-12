from pydantic import BaseModel
from pydantic import Extra 


class Record(BaseModel):
    author: str
    is_submitter: bool
    created_utc: int
    subreddit: str
    score: int
    gilded: bool
    body: str
    body_sha1: str
    permalink: str
    author_premium: str

    class Config:
        extra = Extra.allow
    
    @property
    def post_url(self):
        return '/'.join(self.permalink.split('/')[:-2])

    @property
    def dict(self):
        return {
            "author": self.author,
            "is_submitter": self.is_submitter,
            "created_utc": self.created_utc,
            "subreddit": self.subreddit,
            "score": self.score,
            "gilded": self.gilded,
            "body": self.body,
            "body_sha1": self.body_sha1,
            "permalink": self.permalink,
            "author_premium": self.author_premium
        }
    
    @property
    def post(self):
        return (
            self.author,
            self.subreddit,
            self.is_submitter,
            self.created_utc,
            self.score,
            self.gilded,
            self.body,
            self.body_sha1,
            self.post_url
        )
