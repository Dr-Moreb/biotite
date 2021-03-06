"""
Conservation of *LexA* DNA-binding site
=======================================

The web page on sequence logos on
`Wikipedia <https://en.wikipedia.org/wiki/Sequence_logo#Consensus_logo>`_
shows the sequence logo of the *LexA*-binding motif of Gram-positive
bacteria. In this example we look at the other side: What is the
amino acid sequence logo of the DNA-binding site of the LexA repressor?

We start by searching the NCBI Entrez database for *lexA* gene
entries in the UniProtKB database and downloading them afterwards as
GenPept file.
In order to ensure that the file contains the desired entries, we check
the entires for their definition (title) and source (species).
"""

# Code source: Patrick Kunzmann
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt
import biotite
import biotite.sequence as seq
import biotite.sequence.io.fasta as fasta
import biotite.sequence.io.genbank as gb
import biotite.sequence.graphics as graphics
import biotite.application.clustalo as clustalo
import biotite.database.entrez as entrez
# Search for protein products of LexA gene in UniProtKB/Swiss-Prot database
query =   entrez.SimpleQuery("lexA", "Gene Name") \
        & entrez.SimpleQuery("srcdb_swiss-prot", "Properties")
# Search for the first 200 hits
# More than 200 UIDs are not recommended for the EFetch service
# for a single fetch
uids = entrez.search(query, db_name="protein", number=200)
file_name = entrez.fetch_single_file(uids, biotite.temp_file("gp"),
                              db_name="protein", ret_type="gp")
# The file contains multiple concatenated GenPept files
# -> Usage of MultiFile
multi_file = gb.MultiFile("gp")
multi_file.read(file_name)
# Separate MultiFile into single GenPeptFile instances
files = [f for f in multi_file]
print("Definitions:")
for file in files[:20]:
    print(file.get_definition())
print()
print("Sources:")
for file in files[:20]:
    print(file.get_source())

########################################################################
# The names of the sources are too long to be properly displayed later
# on. Therefore, we write a function that creates a proper abbreviation
# for a species name.

def abbreviate(species):
    # Remove possible brackets
    species = species.replace("[","").replace("]","")
    splitted_species= species.split()
    return "{:}. {:}".format(splitted_species[0][0], splitted_species[1])

print("Sources:")
all_sources = [abbreviate(file.get_source()) for file in files]
for source in all_sources[:20]:
    print(source)

########################################################################
# Much better.
# For the alignment (required for sequence logo) we need to extract the
# slice of the sequence, that belongs to the DNA-binding site.
# Hence, we simply index the each sequence with the feature for the
# binding site and remove those sequences, that do not have a record
# specifying the required feature.
#
# But we have still an issue:
# Some species seem to be overrepresented, as they show up multiple
# times.
# The reason for this is that some species, like *M. tuberculosis*, are
# represented by multiple strains with (almost) equal *LexA* sequences.
# To reduce this bias, we only want each species to occur only a single
# time.
# So we use a set to store the source name of sequences we already
# listed and ignore all further occurences of that source species. 

# List of sequences
binding_sites = []
# List of source species
sources = []
# Set for ignoring already listed sources
listed_sources = set()
for file, source in zip(files, all_sources):
    if source in listed_sources:
        # Ignore already listed species
        continue
    bind_feature = None
    annot_seq = file.get_annotated_sequence(include_only=["Site"])
    # Find the feature for DNA-binding site
    for feature in annot_seq.annotation:
        if "site_type" in feature.qual \
            and feature.qual["site_type"] == "DNA binding":
                bind_feature = feature
    if bind_feature is not None:
        # If the feature is found,
        # get the sequence slice that is defined by the feature...
        binding_sites.append(annot_seq[bind_feature])
        # ...and save the respective source species
        sources.append(source)
        listed_sources.add(source)
print("Binding sites:")
for site in binding_sites[:20]:
    print(site)

########################################################################
# Now we can perform a multiple sequence alignment of the binding site
# sequences. Here we use Clustal Omega to perform this task.
# Since we have up to 200 sequences we visualize only a small portion of
# the alignment.

alignment = clustalo.ClustalOmegaApp.align(binding_sites)
vis = graphics.AlignmentSimilarityVisualizer(alignment[:,:20])
vis.set_alignment_properties(symbols_per_line=25)
vis.add_labels(labels=sources[:20], size=250)
figure = vis.generate()

########################################################################
# Finally we can generate our sequence logo.

logo = graphics.SequenceLogo(alignment, 800, 200)
figure = logo.generate()
plt.show()