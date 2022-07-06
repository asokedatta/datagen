import os
import pandas as pd

vertex_edges = ["Continent", "University", "University_IS_LOCATED_IN_City", "Country", \
"Country_IS_PART_OF_Continent", "Post", "Post_IS_LOCATED_IN_Country","Post_HAS_TAG_Tag", \
"Post_HAS_CREATOR_Person", "Comment", "Comment_REPLY_OF_Comment", "Comment_HAS_CREATOR_Person", \
"Comment_IS_LOCATED_IN_Country", "Comment_REPLY_OF_Post","Comment_HAS_TAG_Tag","Person", \
"Person_WORK_AT_Company", "Person_LIKES_Post", "Person_LIKES_Comment", "Person_KNOWS_Person", \
"Person_HAS_INTEREST_Tag", "Person_STUDY_AT_University", "Person_IS_LOCATED_IN_City", \
"City", "City_IS_PART_OF_Country", "Company", "Company_IS_LOCATED_IN_Country", \
"Forum", "Forum_HAS_TAG_Tag", "Forum_HAS_MEMBER_Person", "Forum_HAS_MODERATOR_Person", \
"Forum_CONTAINER_OF_Post", "Tag", "Tag_HAS_TYPE_TagClass", \
"TagClass", "TagClass_IS_SUBCLASS_OF_TagClass"]

PATH = input("Enter data path # ")

for file in vertex_edges:
    filename = PATH + file + '.csv'
    
    no_of_rows = 0
    with open(filename) as f:
        no_of_rows = sum(1 for line in f)

    print(file+','+str(no_of_rows - 1))