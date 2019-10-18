from lxml import etree
import sys
import re


def Punctuation(string): 
    punctuations = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
    for x in string.lower(): 
        if x in punctuations: 
            string = string.replace(x, "") 
    return string


def create_dic(attri,a,b,dic):
    for i in b['{}_split'.format(attri)]:
        if i.lower() not in dic:
            dic[i.lower()]=[]
            if i in Punctuation(b[attri]).split():
                dic[i.lower()].append({"id":a,"attribute":attri})
        else:
            if i in Punctuation(b[attri]).split():
                dic[i.lower()].append({"id":a,"attribute":attri})


def convert(file_name,output_name):
    lis=[]
    keyword_dic={}
    f=open(file_name)
    tree=etree.parse(f)
    id_list=[]
    for element in tree.xpath('//book[@id]'):
        id_list.append(element.attrib['id'])
    for i in id_list:
        keyword_dic[i]={'author_split':Punctuation(tree.xpath('/catalog/book[@id="{}"]/author'.format(i))[0].text).split(),'author':tree.xpath('/catalog/book[@id="{}"]/author'.format(i))[0].text,
                                'title_split':Punctuation(tree.xpath('/catalog/book[@id="{}"]/title'.format(i))[0].text).split(),'title':tree.xpath('/catalog/book[@id="{}"]/title'.format(i))[0].text,
                                                    'genre_split':Punctuation(tree.xpath('/catalog/book[@id="{}"]/genre'.format(i))[0].text).split(), 'genre':tree.xpath('/catalog/book[@id="{}"]/genre'.format(i))[0].text,
                                                                        'description_split':Punctuation(tree.xpath('/catalog/book[@id="{}"]/description'.format(i))[0].text).split( ),'description':tree.xpath('/catalog/book[@id="{}"]/description'.format(i))[0].text}
                                    
    index_xml=etree.Element('Root')
    

    index_dic={}

    for k1,v1 in keyword_dic.items():
        create_dic('author',k1,v1,index_dic)
        create_dic('title',k1,v1,index_dic)
        create_dic('genre',k1,v1,index_dic)
        create_dic('description',k1,v1,index_dic)
    for k,v in index_dic.items():
        index=etree.SubElement(index_xml,'index')
        keyword=etree.SubElement(index,'keyword').text=k
        books=etree.SubElement(index,'books')
        for i in v:
            book=etree.SubElement(books,'book')
            book_id=etree.SubElement(book,'id').text=i['id']
            etree.SubElement(book,'attribute').text=i['attribute']
    tree=etree.ElementTree(index_xml)
    tree.write(output_name,encoding='UTF-8',xml_declaration=True,pretty_print=True)                           

if __name__ == "__main__":
    if len(sys.argv)<3:
        raise ValueError('The format of input is wrong!')
        sys.exit(0)
    else:
        file_name=sys.argv[1]
        output_name=sys.argv[2]
        convert(file_name,output_name)