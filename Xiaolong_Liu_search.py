from lxml import etree
import sys

def search(filename1,filename2,input_key,output_name):
    keywords=input_key.split()
    results_xml=etree.Element('results')

    f1=open(filename1)
    tree1=etree.parse(f1)
    f2=open(filename2)
    tree2=etree.parse(f2)


    #find common
    if len(keywords)>1:
        dic1={}
        for element in keywords:
            element=element.lower()
            dic={}
            for i in tree2.xpath('/Root/index[keyword="{}"]/books/book/id/text()'.format(element)):
                dic[i]=[]
                attribute_name=tree2.xpath('/Root/index[keyword="{}"]/books/book[id="{}"]/attribute/text()'.format(element,i))
                for e in attribute_name:
                    dic[i].append(e)
            dic1[element]=dic
        
        pair_list=[]
        for k,v in dic1.items():
            for k1,v1 in v.items():
                for i in v1:
                    
                    pair_list.append(str(k1)+' '+str(i))
        
        evidence=set([x for x in pair_list if pair_list.count(x) ==len(dic1)])

        if len(evidence) != 0:
            
        # else:       
            for i in evidence:
                pair=i.split()
                book=etree.SubElement(results_xml,'book',id='{}'.format(pair[0]))
                attribute_content=tree1.xpath('/catalog/book[@id="{}"]/{}/text()'.format(pair[0],pair[1]))
                etree.SubElement(book,'{}'.format(pair[1])).text=attribute_content[0]




        # a=0
        # for k,v in dic.items():
        #     if a==0:
        #         x=v
        #     else:

        #         x=set(x)&set(v)
        #         x=list(x)
        #     a=a+1
        # commom=x
        # one_id=tree2.xpath('/Index/keyword[@keyword="{}"]/book/@*'.format(keywords[0]))[0]
        

        # if len(x)>1:
        #     for i in v:
        #         book=etree.SubElement(results_xml,'book',id='{}'.format(one_id))
        #         attribute_content=tree1.xpath('/catalog/book[@id="{}"]/{}/text()'.format(one_id,i))
        #         etree.SubElement(book,'{}'.format(i)).text=attribute_content[0]
        # else:
        #     book=etree.SubElement(results_xml,'book',id='{}'.format(one_id))
        #     attribute_content=tree1.xpath('/catalog/book[@id="{}"]/{}/text()'.format(one_id,v[0]))
        #     etree.SubElement(book,'{}'.format(v[0])).text=attribute_content[0]



    else:
        dic={}
        for i in tree2.xpath('/Root/index[keyword="{}"]/books/book/id/text()'.format(keywords[0].lower())):
            dic[i]=[]
            attribute_name=tree2.xpath('/Root/index[keyword="{}"]/books/book[id="{}"]/attribute/text()'.format(keywords[0].lower(),i))
            for e in attribute_name:
                dic[i].append(e)
        for k,v in dic.items():
            if len(v)>1:
                book=etree.SubElement(results_xml,'book',id='{}'.format(k))
                for i in v:
                    #book=etree.SubElement(results_xml,'book',id='{}'.format(k))
                    attribute_content=tree1.xpath('/catalog/book[@id="{}"]/{}/text()'.format(k,i))
                    etree.SubElement(book,'{}'.format(i)).text=attribute_content[0]
            else:
                book=etree.SubElement(results_xml,'book',id='{}'.format(k))
                attribute_content=tree1.xpath('/catalog/book[@id="{}"]/{}/text()'.format(k,v[0]))
                etree.SubElement(book,'{}'.format(v[0])).text=attribute_content[0]


    # for element in keywords:
    #     for i in tree2.xpath('/Index/keyword[@keyword="{}"]/book/@*'.format(element)):
    #         # book=etree.SubElement(results_xml,'book',id='{}'.format(i))
    #         attribute_name=tree2.xpath('/Index/keyword[@keyword="{}"]/book[@id="{}"]/attribute/text()'.format(element,i))
    #         for e in attribute_name:
    #             book=etree.SubElement(results_xml,'book',id='{}'.format(i))
    #             attribute_content=tree1.xpath('/catalog/book[@id="{}"]/{}/text()'.format(i,e))
    #             etree.SubElement(book,'{}'.format(e)).text=attribute_content[0]

    tree=etree.ElementTree(results_xml)
    tree.write(output_name,encoding='UTF-8',xml_declaration=True,pretty_print=True)      

if __name__ == "__main__":
    file_name=sys.argv[1]
    output_name=sys.argv[2]
    inputwords=sys.argv[3]
    ouputname=sys.argv[4]
    search(file_name,output_name,inputwords,ouputname)