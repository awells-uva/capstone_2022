def create_training_data(infile, project_id=None, run_accession=None, my_local_path='cwd'):

  import pandas
  import pysam
  import subprocess
  import os
  if my_local_path =='cwd':
    my_local_path = os.getcwd()
  try:
    samfile = pysam.AlignmentFile(infile, "r")
    _ = samfile.fetch()
    samfile.close()
  except:
    samfile.close()
    cmd = [ my_local_path +"samtools/bin/samtools",
      "index", infile
      ]
    print("Running Command: ", *cmd)
    subprocess.run(cmd)
    
  samfile = pysam.AlignmentFile(infile, "r")
  unmapped = []
  for read in samfile.fetch():
    
    if (read.is_unmapped) or (read.flag == 0):
      unmapped.append(read.to_dict())
 
  if len(unmapped) > 0:
    df = pandas.DataFrame.from_records(unmapped)
    df = df.sort_values(by=['name'], ascending=True, ignore_index=True)
    df = df.assign(project_id=project_id)
    df = df.assign(run_accession=run_accession)
    samfile.close()
    return df
  else:
    print("No Unmapped Reads For: Project->{} Run->{}".format(project_id,run_accession ))
    return None

####################
####################

def flag_to_strings(decimal):
  flag_vals = {
    1:		"This is a paired read",
    2:		"This read is part of a pair that aligned properly*",
    4:		"This read was not aligned",
    8:		"This read is part of a pair and its mate was not aligned",
    16:		"This read aligned in the reverse direction**",
    32:		"This read is part of a pair and its mate aligned in the reverse direction**",
    64:		"This read is the first in the pair (read 1)",
    128:	"This read is the second in pair (read 2)",
    256:	"The given alignment is a secondary alignment***",
    512:	"Read failed quality check (such as Illumina quality filtering)",
    1024:	"Read was flagged as a duplicate (such as a PCR duplicate)",
    2048:	"Supplementary alignment (Exact meaning varies by aligner)"
  }
  if decimal in flag_vals.keys() or decimal == 1:
    string = flag_vals[decimal]
    return string
  if int(decimal) > 2048:
    string = "Unknown Flag Value: {}".format(decimal)
    return string
  string = ''
  binary_val = bin(decimal).replace("0b", "")
  for i,val in enumerate(binary_val[::-1]):
    if int(val):
      string = string + flag_vals[2**(i)] + '\n'
  return string

####################
####################

def build_kmers(sequence, ksize):
    kmers = []
    n_kmers = len(sequence) - ksize + 1

    for i in range(n_kmers):
        kmer = sequence[i:i + ksize]
        kmers.append(kmer)

    return kmers

####################
####################

# https://neo4j.com/docs/graph-data-science/current/alpha-algorithms/jaccard/
def jaccard_similarity(a, b):
    """
    Jaccard Similarity (coefficient), a term coined by Paul Jaccard, 
    measures similarities between sets. It is defined as the size of the 
    intersection divided by the size of the union of two sets. 
    This notion has been generalized for multisets, 
    where duplicate elements are counted as weights.
    """

    a = set(a)
    b = set(b)

    intersection = len(a.intersection(b))
    union = len(a.union(b))

    return intersection / union

####################
####################

def jaccard_containment(a, b):
    a = set(a)
    b = set(b)

    intersection = len(a.intersection(b))

    return intersection / len(a)

####################
####################

def read_kmers_from_list(array, ksize):
  all_kmers = []
  for sequence in array:
    kmers = build_kmers(sequence, ksize)
    all_kmers += kmers
  return all_kmers

####################
####################

def cosine_similarity(arr1, arr2):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    count_vectorizer = CountVectorizer()
    vector_matrix = count_vectorizer.fit_transform([' '.join(str(x) for x in arr1), ' '.join(str(x) for x in arr2)])
    tokens = count_vectorizer.get_feature_names()
    cosine_similarity_matrix = cosine_similarity(vector_matrix)
    
    return cosine_similarity_matrix[0][1]

####################
####################

def get_location_data(project_ID):
    import requests
    import json
    import pandas
    url = 'https://www.ebi.ac.uk/ena/portal/api/filereport'
    params = {'accession':"{}".format(project_ID),
              'fields':"center_name,instrument_platform,instrument_model,host",
            'format':'json',
            'download':'false',
            'result':'read_run'}
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"+
             " AppleWebKit/537.36 (KHTML, like Gecko)"+
             " Chrome/70.0.3538.77 Safari/537.36"}

    print("Accessing: ", url)
    r = requests.get(url,
                  params = params,
                  headers = headers
                  ) 
    print("\tMaking Request To: ", r.url) 
    my_json = json.loads(r.text)
    df = pandas.json_normalize(json.loads(r.text))
    df = df.assign(project_id=project_ID)
    
    # Temp Fix if center_name field is empty
    df['center_name'] = df['center_name'].replace('', project_ID)
    return df

####################
####################

def clean_seq(sequences, K):
    tmp = []
    nucleotides = [x*K for x in ['A','C','G','T','N']]
    ##### BEGIN TEST WITH DOUBLES #####
    #from itertools import combinations
    #combs = list(combinations(['A','C','G','T','N'], 2))
    #temp = [ "{}{}".format(x[0],x[1]) for x in combs] + [ "{}{}".format(x[1],x[0]) for x in combs]
    #temp = [x*K for x in temp]
    #temp = [x[:K] for x in temp]
    #nucleotides = nucleotides + temp
    ##### END TEST WITH DOUBLES #####
    #print(nucleotides)
    for sequence in sequences:
        if any([True if repeated_nucleotide in sequence else False for repeated_nucleotide in nucleotides ]):
            continue
        else:
            tmp.append(sequence)   
    return tmp

####################
####################

def plot_similarity_matrix(similarity_matrix,color_map = "spring", title = "Similarity Matrix", filename = "Similarity_Matrix.png"):
    import numpy
    import matplotlib.pyplot as plt
    import seaborn

    # Generate a mask for the upper triangle
    mask = numpy.triu(numpy.ones_like(similarity_matrix, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(20, 20))

    # Draw the heatmap with the mask and correct aspect ratio
    seaborn.heatmap(similarity_matrix, cmap = color_map, mask=mask, ax=ax);

    ax.set_title(title)
    plt.tight_layout()
    #plt.show();
    plt.savefig(filename);
    
