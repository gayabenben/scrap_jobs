import re
import numpy as np

from job_offer import JobOffer

JobOffer.fetch_html("https://emploi.cnrs.fr/OffreEmploi.aspx?LieuTravail=13&OffreId=56152&Lang=FR")