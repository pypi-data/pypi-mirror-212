from typing import List
from typing import Optional

from pydantic.fields import Field

from .base import BaseModelORM

class Technology(BaseModelORM):
    Category: str
    Name: str


class SemrushData(BaseModelORM):
    semrush_rank: int
    organic_keywords: int
    organic_traffic: int
    organic_cost: int


class DailyEarning(BaseModelORM):
    country: str
    earnings_in_usd: float
    page_views: int


class Revenue(BaseModelORM):
    daily_revenue_in_usd: float
    monthly_revenue_in_usd: float
    yearly_revenue_in_usd: float


class Blocked(BaseModelORM):
    daily_page_views: int
    monthly_page_views: int
    yearly_page_views: int


class DailyItem(BaseModelORM):
    country: str
    usd: float
    blocked: int


class AdblockLoss(BaseModelORM):
    revenue: Revenue
    blocked: Blocked
    daily: List[DailyItem]


class RevenueReport(BaseModelORM):
    daily_in_usd: float
    monthly_in_usd: float
    yearly_in_usd: float
    daily_earnings: List[DailyEarning]
    adblock_loss: AdblockLoss


class Supports(BaseModelORM):
    ssl: bool
    http2: bool


class MywotReputationReport(BaseModelORM):
    status: str
    safety_reputations: int
    safety_confidence: int
    child_safety_reputations: int
    child_safety_confidence: int


class ServerData(BaseModelORM):
    ip: str
    asn: str
    isp: str
    location: str
    other_sites_hosted_on_this_server: List[str]
    average_load_time_in_ms: int


class SearchEngine(BaseModelORM):
    name: str
    count: int


class Country(BaseModelORM):
    country: str
    domains: int


class Tld(BaseModelORM):
    tld: str
    domains: int


class BacklinkgsReport(BaseModelORM):
    total: int
    follow: int
    nofollow: int
    referring_domain: int
    referring_ips: int
    authority_domain_score: int
    countries: List[Country]
    tlds: List[Tld]


class Visitor(BaseModelORM):
    domain: str
    per_user: float
    per_user_rate: float
    formatted_per_user_rate: str
    reach_rate: float
    formatted_reach_rate: str


class MozData(BaseModelORM):
    domain_authority: int
    page_authority: int
    moz_rank: int


class Traffic(BaseModelORM):
    global_reach: float
    formatted_global_reach: str
    monthly_visits_by_semrush: int
    formatted_monthly_visits_by_semrush: str
    monthly_unique_visitors_by_semrush: int
    formatted_monthly_unique_visitors_by_semrush: str
    semrush_rank: int


class DesktopVsMobile(BaseModelORM):
    desktop: float
    formatted_desktop: str
    mobile: float
    formatted_mobile: str


class Data(BaseModelORM):
    description: str
    about: str
    technologies: List[Technology]
    semrush_data: SemrushData
    revenue_report: RevenueReport
    related_sites: List[str]
    supports: Supports
    mywot_reputation_report: MywotReputationReport
    server_data: ServerData
    website_value: int
    search_engines: List[SearchEngine]
    backlinkgs_report: BacklinkgsReport
    visitors: List[Visitor]
    moz_data: MozData
    traffic: Traffic
    desktop_vs_mobile: DesktopVsMobile


class AdditionalDomainDataModel(BaseModelORM):
    description: str
    status: int
    data: Data
