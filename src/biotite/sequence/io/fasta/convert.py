# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

__author__ = "Patrick Kunzmann"

from ...sequence import Sequence
from ...alphabet import AlphabetError, LetterAlphabet
from ...seqtypes import NucleotideSequence, ProteinSequence
from ...align.alignment import Alignment

__all__ = ["get_sequence", "get_sequences", "set_sequence", "set_sequences",
           "get_alignment", "set_alignment"]


def get_sequence(fasta_file, header=None):
    """
    Get a sequence from a `FastaFile` instance.
    
    Parameters
    ----------
    fasta_file : FastaFile
        The `FastaFile` to be accessed.
    header : str, optional
        The header to get the sequence from. By default, the first
        sequence of the file is returned.
    
    Returns
    -------
    sequence : `NucleotideSequence` or `ProteinSequence`
        The first sequence in the `FastaFile`.
        `NucleotideSequence` if the sequence string fits the
        corresponding alphabet, `ProteinSequence` otherwise.
    
    Raises
    ------
    ValueError
        If the sequence data can be neither converted into a
        `NucleotideSequence` nor a `ProteinSequence`.
    """
    if header is not None:
        seq_str = fasta_file[header]
    else:
        # Return first (and probably only) sequence of file
        seq_str = None
        for header, seq_str in fasta_file:
            break
        if seq_str is None:
            raise ValueError("File does not contain any sequences")
    # Determine the sequence type:
    # If NucleotideSequence can be created it is a DNA sequence,
    # otherwise protein sequence
    return _convert_to_sequence(seq_str)


def get_sequences(fasta_file):
    """
    Get dictionary from a `FastaFile` instance,
    where headers are keys and sequences are values.
    
    Parameters
    ----------
    fasta_file : FastaFile
        The `FastaFile` to be accessed.
    
    Returns
    -------
    seq_dict : dict
        A dictionary containg `NucleotideSequence` and/or
        `ProteinSequence` instances.
    
    Raises
    ------
    ValueError
        If at least on of the sequence strings can be neither converted
        into a `NucleotideSequence` nor a `ProteinSequence`.
    """
    seq_dict = {}
    for header, seq_str in fasta_file:
        seq_dict[header] = _convert_to_sequence(seq_str)
    return seq_dict


def set_sequence(fasta_file, sequence, header=None):
    """
    Set a sequence in a `FastaFile` instance.
    
    Parameters
    ----------
    fasta_file : FastaFile
        The `FastaFile` to be accessed.
    sequence : Sequence
        The sequence to be set.
    header : str, optional
        The header for the sequence. Default is 'sequence'.
    
    Raises
    ------
    ValueError
        If the sequence's alphabet uses symbols other than single
        letters.
    """
    if header is None:
        header = "sequence"
    fasta_file[header] = _convert_to_string(sequence)


def set_sequences(fasta_file, sequence_dict):
    """
    Set sequences in a `FastaFile` instance from a dictionary.
    
    Parameters
    ----------
    fasta_file : FastaFile
        The `FastaFile` to be accessed.
    sequence_dict : dict
        A dictionary containing the sequences to be set.
        Header are keys, `Sequence` instances are values. 
    
    Raises
    ------
    ValueError
        If the sequences alphabets uses symbols other than single
        letters.
    """
    for header, sequence in sequence_dict.items():
        fasta_file[header] = _convert_to_string(sequence)


def get_alignment(fasta_file, additional_gap_chars=("_",)):
    """
    Get an alignment from a `FastaFile` instance.
    
    Parameters
    ----------
    fasta_file : FastaFile
        The `FastaFile` to be accessed.
    additional_gap_chars : str, optional
        The characters to be treated as gaps.
    
    Returns
    -------
    alignment : Alignment
        The alignment from the `FastaFile`.
    """
    seq_strings = [seq_str for header, seq_str in fasta_file]
    # Replace additional gap symbols with default gap symbol ('-')
    for char in additional_gap_chars:
        for i, seq_str in enumerate(seq_strings):
            seq_strings[i] = seq_str.replace(char, "-")
    # Remove gaps for creation of sequences
    sequences = [_convert_to_sequence(seq_str.replace("-",""))
                 for seq_str in seq_strings]
    trace = Alignment.trace_from_strings(seq_strings)
    return Alignment(sequences, trace, score=None)


def set_alignment(fasta_file, alignment, seq_names):
    """
    Fill a `FastaFile` with gapped sequence strings from an alignment.
    
    Parameters
    ----------
    fasta_file : FastaFile
        The `FastaFile` to be accessed.
    alignment : Alignment
        The alignment to be set. 
    seq_names : iterable object of str
        The names for the sequences in the alignment.
        Must have the same length as the sequence count in `alignment`.
    """
    gapped_seq_strings = alignment.get_gapped_sequences()
    if len(gapped_seq_strings) != len(seq_names):
        raise ValueError(
            f"Alignment has {len(gapped_seq_strings)} sequences, "
            f"but {len(seq_names)} names were given"
        )
    for i in range(len(gapped_seq_strings)):
        fasta_file[seq_names[i]] = gapped_seq_strings[i]


def _convert_to_sequence(seq_str):
    try:
        code = NucleotideSequence.alphabet.encode_multiple(seq_str)
        seq = NucleotideSequence()
        seq.code = code
        return seq
    except AlphabetError:
        pass
    try:
        code = ProteinSequence.alphabet.encode_multiple(seq_str)
        seq = ProteinSequence()
        seq.code = code
        return seq
    except AlphabetError:
        pass
    try:
        code = NucleotideSequence.alphabet_amb.encode_multiple(seq_str)
        seq = NucleotideSequence()
        seq.code = code
        return seq
    except AlphabetError:
        raise ValueError("FASTA data cannot be converted either to "
                         "'NucleotideSequence' nor to 'ProteinSequence'")


def _convert_to_string(sequence):
    if not isinstance(sequence.get_alphabet(), LetterAlphabet):
        raise ValueError("Only sequences using single letter alphabets "
                         "can be stored in a FASTA file")
    return(str(sequence))