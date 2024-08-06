import nltk
from nltk import grammar, parse
import argparse

from nlp_parser import parse_to_procedure
from nlp_data import retrieve_result
from nlp_file import write_file
from nltk.parse.generate import generate

def main(args):
    """
    Main entry point for the program
    """
    #Load grammar from .fcfg file
    print("-------------Loading grammar---------------------")
    nlp_grammar = parse.load_parser(args.rule_file_name, trace = 0)
    print("Grammar loaded at {}".format(args.rule_file_name))
    
    print("-------------Loading Sentence file---------------------")
    with open('input/sentences.txt', 'r', encoding="utf8") as file:
      sentences = file.read()

    sentences = sentences.split('\n')
    parse_result = ''
    for sentence in sentences:
        tree = nlp_grammar.parse_one(sentence.replace('?','').split())
        if tree is None: tree = []
        parse_result += str(tree) + "\n"
    
    write_file('output/parse_result.txt', parse_result)
    print("PASS")
               
    question = args.question
    
    #Get parse tree
    print("-------------Parsed structure-------------")
    tree = nlp_grammar.parse_one(question.replace('?','').split())
    print(question)
    print(tree)
    
    #Produce sentence
    print("-------------Parsed structure-------------")
    
    
    #Parse to logical form
    print("-------------Parsed logical form-------------")
    logical_form = str(tree.label()['SEM']).replace(',',' ')
    print(logical_form)
    
    #Get procedure semantics
    print("-------------Procedure semantics-------------")
    procedure_semantics = parse_to_procedure(tree)
    print(procedure_semantics)
    
    #Retrive result:
    print("-------------Retrieved result-------------")
    results, question_type = retrieve_result(procedure_semantics)
    print(results)
    file_name = f"output/p2-q-{question_type}.txt"
    write_file(file_name, results)

    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NLP Assignment Command Line")
    
    parser.add_argument(
      '--question',
      default= "đi Nha Trang có những ngày nào nhỉ?",
      help= "Question to be parsed.'"
      )
    
    parser.add_argument(
      '--rule_file_name',
      default= "grammar.fcfg",
      help= "Context Free Grammar file to be parsed. Default = 'grammar.fcfg'"
      )
    
    args = parser.parse_args()
    main(args)
