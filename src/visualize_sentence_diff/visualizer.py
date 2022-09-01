from typing import List, Tuple
from difflib import Differ

import spacy
import spacy.lang.en
from IPython.display import HTML, display


nlp = None
spacy_package = "en_core_web_sm"
def get_spacy_nlp() -> spacy.lang.en.English:
    global nlp
    if not nlp:
        try:
            nlp = spacy.load(spacy_package)
        except:
            import subprocess
            subprocess.run("python3 -m spacy download %s" % spacy_package, shell=True)
            nlp = spacy.load(spacy_package)
    return nlp


def diff_html_from_sign(token_list: List[str], sign_list: List[int],
                        tag_front: str='<span>', tag_back: str='</span>') -> str:
    assert len(token_list) == len(sign_list)
    
    output_list = []
    for st, sign in zip(token_list, sign_list):
        if sign == 0:
            output_list.append(st)
        elif sign == 1:
            output_list.append(tag_front + st + tag_back)
        else:
            raise ValueError()
    
    return " ".join(output_list)


def compuare_sentence_and_generate_html(sentence_x: str, sentence_y: str, transparency: float=.5) -> Tuple[str, str]:
    spacy_nlp = get_spacy_nlp()
    list_x = [str(s) for s in list(spacy_nlp(sentence_x))]
    list_y = [str(s) for s in list(spacy_nlp(sentence_y))]
    
    # diff
    differ = Differ()
    diff_list = list(differ.compare(list_x, list_y))
    
    sign_for_x, sign_for_y = [], []
    for d in diff_list:
        if d[0] == " ":
            sign_for_x.append(0)
            sign_for_y.append(0)
        if d[0] == "-":
            sign_for_x.append(1)
        if d[0] == "+":
            sign_for_y.append(1)
    
    # html
    x_html = diff_html_from_sign(token_list=list_x, sign_list=sign_for_x,
                                 tag_front=f'<span style="background-color:rgba(255,0,0,{transparency})">')
    y_html = diff_html_from_sign(token_list=list_y, sign_list=sign_for_y,
                                 tag_front=f'<span style="background-color:rgba(0,255,0,{transparency})">')

    return x_html, y_html


def visualize_sentence_diff(sentence_x: str, sentence_y: str) -> None:
    html_x, html_y = compuare_sentence_and_generate_html(sentence_x, sentence_y)

    output_html = f'''
        <table>
            <tr>
                <td>sentence x</td>
                <td>sentence y</td>
            </tr>
            <tr>
                <td>{html_x}</td>
                <td>{html_y}</td>
            </tr>
        </table>
    '''

    display(HTML(output_html))
