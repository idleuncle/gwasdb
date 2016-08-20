"""Load and parse EFO ontology into database

This parse the EFO csv file into Phenotype objects.
  name: receives the main EFO name
  synonyms: join of synonyms on '|'
  source: 'efo'
  ontology_ref: the EFO id
"""


import argparse
import string
import unicodedata

from sqlalchemy.sql import exists, and_, or_

from db import db_session
from db.schema import *

# ----------------------------------------------------------------------------

def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('--init', action='store_true', help='Init db')
  parser.add_argument('--csv', help='Load phenotype/ontology mapping')
  args = parser.parse_args()

  if args.init:
    init_db()

  if args.csv:
    parse_ontology(args.csv, db_session)

def parse_ontology(fname, db_session):
  phenotypes = set()
  with open(fname) as f:
    f.readline()
    for line in f:
      fields = line.split(',')
      ontology_id = fields[0]
      name = _normalize_str(fields[1])
      synonyms = _normalize_str(fields[2])
      # print line
      # print fields
      
      db_session.add(
        Phenotype(
          name=name,
          source='efo',
          synonyms=synonyms,
          ontology_ref=ontology_id
        )
      )
  
  db_session.commit()

def _normalize_str(s):
  s = s.decode('utf-8')
  s = unicodedata.normalize('NFKD', s).encode('ascii','ignore')
  # print s
  return s
  # return unicode(s)


# ----------------------------------------------------------------------------

if __name__ == '__main__':
  main()