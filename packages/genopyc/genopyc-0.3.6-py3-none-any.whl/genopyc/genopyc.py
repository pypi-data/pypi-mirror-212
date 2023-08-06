import requests
import pandas as pd
from tqdm import tqdm
import numpy as np


def get_associations(efotrait,verbose=False):
    """Retrieve snps associated to an EFO trait"""
    df=pd.DataFrame(columns=['variantid','p-value','risk_allele','RAF','beta','CI','mapped_gene'])
    http= 'https://www.ebi.ac.uk/gwas/rest/api/efoTraits/%s/associations' %(efotrait)
    if verbose:
        print('querying associations... \n')
    resp=requests.get(http)
    if resp.ok:
        associ=resp.json()
        if verbose:
            print('building the dataframe...')
        for i,element in enumerate(associ['_embedded']['associations']):
            try:
                df.at[i,'variantid']=''.join(element['loci'][0]['strongestRiskAlleles'][0]['riskAlleleName'].split('-')[0:1])
                df.at[i,'risk_allele']=element['loci'][0]['strongestRiskAlleles'][0]['riskAlleleName'].split('-')[-1]
                df.at[i,'mapped_gene']=[e['geneName'] for e in element['loci'][0]['authorReportedGenes']]
                df.at[i,'p-value']=float(element['pvalueMantissa'])*10**int(element['pvalueExponent'])
                try: 
                    df.at[i,'RAF']=float(element['riskFrequency'])
                except:
                    df.at[i,'RAF']=np.nan
                    
                df.at[i,'beta']=[float(element['betaNum']) if type(element['betaNum'])==float else np.nan][0]
                df.at[i,'SE']=element['standardError']
                df.at[i,'CI']=element['range']
            except Exception as e:
                print(f'error {e} for element {element}')
                pass
        df.fillna(np.nan, method = None,inplace = True)
        df['p-value'] = df['p-value'].map("{:.1e}".format)

        return df
    else:
         print(f'ERROR: Bad Resquest: \n {resp}')



#retrieve the coordinates of many genes
def get_gene_position_many(idlist,chunked=False,chunksize=200):

    """ This function accept a list of ensembl Ids and return the coordinates in the GHRC38 if the list is longer than 200 it needs to be chunked because ensembl accepts maximum a request of 200 Ids per time"""

    http="https://rest.ensembl.org/lookup/id"
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    if chunked | len(idlist) > 200 :
        chunked_idlist=[]
        print('total number of chunks: %s' %(int(len(idlist)/chunksize)+1))
        for i in range(0,len(idlist),chunksize):
            chunked_idlist.append(idlist[i:i+chunksize])
        results=[]
        for i,chunk in enumerate(chunked_idlist):
            response = requests.post(http, headers=headers, 
                                     data="{" + '"ids" : {}'.format(str(chunk).replace("'",'"'))+"}").json()

            ListOfTuples=[]
            for k,v in response.items():
                try:
                    ListOfTuples.append((k,int(v['seq_region_name']),v['start'],v['end']))

                except:

                    print(f"Couldn't retrieve position for gene {k}") 
                    continue

            results.append(ListOfTuples)
            print('chunk %s processed' % (i))
        return sum(results,[])
    else:
        response = requests.post(http, headers=headers, 
                                     data="{" + '"ids" : {}'.format(str(idlist).replace("'",'"'))+"}").json()

        ListOfTuples=[]

        for k,v in response.items():
            try:
                ListOfTuples.append((k,int(v['seq_region_name']),v['start'],v['end']))
            except:

                print(f"Couldn't retrieve position for gene {k}") 
                pass
        return ListOfTuples

def get_variant_position_many(idlist,chunked=False,chunksize=200):
    http="https://rest.ensembl.org/variation/homo_sapiens"
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    if chunked | len(idlist) > 200:
        chunked_idlist=[]
        print('total number of chunks: %s' %(int(len(idlist)/chunksize)+1))
        for i in range(0,len(idlist),chunksize):
            chunked_idlist.append(idlist[i:i+chunksize])
        results=[]
        for i,chunk in enumerate(chunked_idlist):
            response = requests.post(http, headers=headers, 
                                     data="{" + '"ids" : {}'.format(str(chunk).replace("'",'"'))+"}").json()
            for key,value in response.items():
                try:
                    chr=value['mappings'][0]['location'].split(':')[0]
                    pos=value['mappings'][0]['start']
                    results.append((key,chr,pos))
                
                except:
                    print(f"Couldn't Retrieve Position for variant {key}")
                    pass
            print(f"chunk {i} processed")        
        return results        
            
    else:
        response = requests.post(http, headers=headers, 
                                     data="{" + '"ids" : {}'.format(str(idlist).replace("'",'"'))+"}").json()

        results=[]
        for key,value in response.items():
            try:
                chr=value['mappings'][0]['location'].split(':')[0]
                pos=value['mappings'][0]['start']
                results.append((key,chr,pos))
            
            except:
                print(f"Couldn't Retrieve Position for variant {key}")
                pass        
        return results


def HGVS_VEP(idlist, chunked=False,chunksize=200,verbose=False,all_data=False):
    '''Variants must be fed in HGVS notation that is cr:glocREF>ALT'''
    http="https://rest.ensembl.org/vep/human/hgvs"
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    chunked_idlist=[]
    if chunked | len(idlist) > 200:
        print('total number of chunks: %s' %(int(len(idlist)/chunksize)+1))
        for i in range(0,len(idlist),chunksize):
            chunked_idlist.append(idlist[i:i+chunksize])
        results=[]
        for i,chunk in enumerate(chunked_idlist):
            response = requests.post(http, headers=headers, 
                                     data="{" + '"hgvs_notations" : {}'.format(str(chunk).replace("'",'"'))+"}")
            results.append(response.json())
            print('chunk %s processed' % (i))
    
        req_results=sum(results,[])
    else:
        results = requests.post(http, headers=headers, 
                                     data="{" + '"hgvs_notations" : {}'.format(str(idlist).replace("'",'"'))+"}")
        req_results=results.json()
    
    
    final_transcript_consequences=[]
    final_intergenic_consequences=[]
    final_regulatory_feature_consequences=[]
    final_motif_consequences=[]
    for dict_of_resu in req_results:
        variant_id=dict_of_resu['input']
        #Check Transcript Consequences
        try:
            transcript_consequences=dict_of_resu['transcript_consequences']
            for tc in transcript_consequences :
                consequence_terms=tc['consequence_terms']
                gene_id=tc['gene_id']
                biotype=tc['biotype']
                final_transcript_consequences.append((variant_id,consequence_terms,biotype,gene_id))

            n_of_tc=len(transcript_consequences)
        except Exception as error:
            n_of_tc=0



        #Check Intergenic Consequences
        try:
            intergenic_consequences=dict_of_resu['intergenic_consequences']
            for ic in intergenic_consequences :
                consequence_terms=ic['consequence_terms']
                impact=ic['impact']
                final_intergenic_consequences.append((variant_id,consequence_terms,impact))
                n_of_ic=len(intergenic_consequences)


        except Exception as error:
            n_of_ic=0




        #Check regulatory_feature_consequences
        try:
            regulatory_feature_consequences=dict_of_resu['regulatory_feature_consequences']

            for rfc in regulatory_feature_consequences :
                consequence_terms=rfc['consequence_terms']
                impact=rfc['impact']
                biotype=rfc['biotype']
                final_regulatory_feature_consequences.append((variant_id,consequence_terms,biotype,impact))
                n_of_rfc=len(regulatory_feature_consequences)


        except Exception as error:
            n_of_rfc=0
        
        #Check motif feature consequences
        try:
            motif_consequences=dict_of_resu['motif_feature_consequences']

            for mfc in motif_consequences :
                consequence_terms=mfc['consequence_terms']
                tf=mfc['transcription_factors']
                impact=mfc['motif_score_change']
                final_motif_consequences.append((variant_id,consequence_terms,tf,impact))
                n_of_mfc=len(motif_consequences)


        except Exception as error:
            n_of_mfc=0



        if verbose:
            print(f"{variant_id} has {n_of_tc} transcript consquence, {n_of_ic} intergenic consquence, {n_of_rfc} regulatory feature consequence, {n_of_mfc} motif feature consequences")

    if all_data:
        return req_resu
    
    return final_transcript_consequences, final_regulatory_feature_consequences, final_intergenic_consequences,final_motif_consequences
        

        

def VEP(idlist, chunked=False,chunksize=200,verbose=False,all_data=False):
    http="https://rest.ensembl.org/vep/human/id/"
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    chunked_idlist=[]
    if chunked | len(idlist) > 200:
        print('total number of chunks: %s' %(int(len(idlist)/chunksize)+1))
        for i in range(0,len(idlist),chunksize):
            chunked_idlist.append(idlist[i:i+chunksize])
        results=[]
        for i,chunk in enumerate(chunked_idlist):
            response = requests.post(http, headers=headers, 
                                     data="{" + '"ids" : {}'.format(str(chunk).replace("'",'"'))+"}")
            results.append(response.json())
            print('chunk %s processed' % (i))
    
        req_results=sum(results,[])
    else:
        results = requests.post(http, headers=headers, 
                                     data="{" + '"ids" : {}'.format(str(idlist).replace("'",'"'))+"}")
        req_results=results.json()
    
    
    final_transcript_consequences=[]
    final_intergenic_consequences=[]
    final_regulatory_feature_consequences=[]
    final_motif_consequences=[]

    for dict_of_resu in req_results:
        variant_id=dict_of_resu['input']
        #Check Transcript Consequences
        try:
            transcript_consequences=dict_of_resu['transcript_consequences']
            for tc in transcript_consequences :
                consequence_terms=tc['consequence_terms']
                gene_id=tc['gene_id']
                biotype=tc['biotype']
                final_transcript_consequences.append((variant_id,consequence_terms,biotype,gene_id))

            n_of_tc=len(transcript_consequences)
        except Exception as error:
            n_of_tc=0



        #Check Intergenic Consequences
        try:
            intergenic_consequences=dict_of_resu['intergenic_consequences']
            for ic in intergenic_consequences :
                consequence_terms=ic['consequence_terms']
                impact=ic['impact']
                final_intergenic_consequences.append((variant_id,consequence_terms,impact))
                n_of_ic=len(intergenic_consequences)


        except Exception as error:
            n_of_ic=0




        #Check regulatory_feature_consequences
        try:
            regulatory_feature_consequences=dict_of_resu['regulatory_feature_consequences']

            for rfc in regulatory_feature_consequences :
                consequence_terms=rfc['consequence_terms']
                impact=rfc['impact']
                biotype=rfc['biotype']
                final_regulatory_feature_consequences.append((variant_id,consequence_terms,biotype,impact))
                n_of_rfc=len(regulatory_feature_consequences)


        except Exception as error:
            n_of_rfc=0
        
        #Check motif feature consequences
        try:
            motif_consequences=dict_of_resu['motif_feature_consequences']

            for mfc in motif_consequences :
                consequence_terms=mfc['consequence_terms']
                tf=mfc['transcription_factors']
                impact=mfc['motif_score_change']
                final_motif_consequences.append((variant_id,consequence_terms,tf,impact))
                n_of_mfc=len(motif_consequences)


        except Exception as error:
            n_of_mfc=0



        if verbose:
            print(f"{variant_id} has {n_of_tc} transcript consquence, {n_of_ic} intergenic consquence, {n_of_rfc} regulatory feature consequence, {n_of_mfc} motif feature consequences")

    if all_data:
        return req_resu
    
    return final_transcript_consequences, final_regulatory_feature_consequences, final_intergenic_consequences,final_motif_consequences
    
        
        
#Retrieves variant in LD with a given variant
def get_variants_in_LD(variant,r2,pop='EUR'):
    http= "https://rest.ensembl.org/ld/human/%s/1000GENOMES:phase_3:%s?r2=%s" %(variant,pop,r2)
    try:
        variants=requests.get(http,headers={ "Content-Type" : "application/json"}).json()

        return [x['variation2'] for x in variants if float(x['r2'])>=r2]
    except:
        pass

    
    
    
def GetLDMatrix(ListOfSnps,token,pop='EUR',metric='r2'):
    SnpString='\n'.join(ListOfSnps)

    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('token', token),
    )

    json_data = {
        'snps': SnpString,
        'pop': pop,
        'r2_d': metric,
        'genome_build': 'grch38',
    }

    response = requests.post('https://ldlink.nci.nih.gov/LDlinkRest/ldmatrix', headers=headers, params=params, json=json_data, verify=False).text
    dataf=pd.DataFrame([x.split('\t') for x in response.split('\n')])
    new_header=dataf.iloc[0]
    dataf= dataf[1:] #take the data less the header row
    dataf.columns = new_header #set the header row as the df header
    
    new_rows=dataf[dataf.columns[0]]
    dataf=dataf[dataf.columns[1:]].set_index(new_rows)
    
    dataf.replace('NA',None,inplace = True)
    dataf =dataf.astype(None)
    
    return dataf.fillna(0).iloc[:-1]
    
    
    
def PairwiseLD(ch,start,end,pop = 'EUR'):
    http= f"https://rest.ensembl.org/ld/human/region/{ch}:{str(start)}..{str(end)}/1000GENOMES:phase_3:{pop}"
    response = requests.get(http,headers={ "Content-Type" : "application/json"}).json()
    ldmat = []
    
    
    for i,element in enumerate(response):
        try:
            v1 = element['variation1']
            v2 = element['variation2']
            r2 = element['r2']
            ldmat.append((v1,v2,r2))
        except Exception as r:
            print(r,f'- Error for variant "{element}"')
        ldmatdf = pd.DataFrame(ldmat,columns=['v1','v2','r2'])
        
        


        
    
    
    return ldmatdf.sort_values(by = 'v1')
   
    

#Retrieve summary statistic of a given study    
def get_summary_statistic(study):
    http= 'https://www.ebi.ac.uk/gwas/summary-statistics/api/studies/%s/associations' %(study)
    ss=requests.get(http).json()
    return ss


#Retrieves the list of studies with summary statistics available for a given trait
def get_summary_statistic_list():
    http= 'https://www.ebi.ac.uk/gwas/summary-statistics/api/associations'
    ss=requests.get(http).json()
    return ss

#Retrieves annotations of a given genomic region
def get_phenotypes(chromosome,start,stop,feature_type='Genes',only_phenotypes=1):
    http="https://rest.ensembl.org/phenotype/region/homo_sapiens/%s:%s-%s?only_phenotypes=%s;feature_type=%s"%(chromosome,start,stop,only_phenotypes,feature_type)
    annot=requests.get(http, headers={ "Content-Type" : "application/json"})
    return annot.json()

#Retrieves overlapping elements of a given region 
def get_ov_region(chromosome,start,stop,features=list):
    str_features=';'.join(['feature='+x for x in features])
    http="https://rest.ensembl.org/overlap/region/human/%s:%s-%s?%s"%(chromosome,start,stop,str_features)
    risposta=requests.get(http,headers={ "Content-Type" : "application/json"}).json()
    return risposta

#Retrieves the nucleotide sequence of a given position 
def get_sequence(chromosome,start,stop):
    http="https://rest.ensembl.org/sequence/region/human/%s:%s..%s?" %(chromosome,start,stop)
    risposta=requests.get(http,headers={ "Content-Type" : "application/json"}).json()
    return risposta['seq']

## lift from grch37 to 38
def grch_liftover(chromosome,start,end,source,target):
    url="https://rest.ensembl.org/map/human/%s/%s:%i..%i/%s?"%(source,chromosome,start,end,target)
    r = requests.get(url, headers={ "Content-Type" : "application/json"}).json()
    try:
        return (chromosome,r['mappings'][0]['mapped']['start'],r['mappings'][0]['mapped']['end'])
    except:
        return None

## function to get variant list of eqtls
def get_eqtl_variant(rsid):
    url='http://www.ebi.ac.uk/eqtl/api/associations/%s'%(rsid)
    risp=requests.get(url).json()
    return risp
## return single variant info ##
def get_variant_info(variant):
    http= "https://rest.ensembl.org/variation/human/%s?"%(variant)
    associ=requests.get(http,headers={ "Content-Type" : "application/json"}).json()
    return associ

def get_variant_info_many(idlist, chunked=False,chunksize=200):
    http="https://rest.ensembl.org/variation/homo_sapiens"
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    chunked_idlist=[]
    if chunked | len(idlist)>200:
        print('total number of chunks: %s' %(int(len(idlist)/chunksize)+1))
        for i in range(0,len(idlist),chunksize):
            chunked_idlist.append(idlist[i:i+chunksize])
        results={}
        for i,chunk in enumerate(chunked_idlist):
            response = requests.post(http, headers=headers, 
                                     data="{" + '"ids" : {}'.format(str(chunk).replace("'",'"'))+"}")
            results.update(response.json())
            print('chunk %s processed' % (i))
        return results

    else:
        response = requests.post(http, headers=headers, 
                                     data="{" + '"ids" : {}'.format(str(idlist).replace("'",'"'))+"}")
        return response.json()


def get_eqtl_df(rsid,p_value=0.005,increase_index=False):
    url='http://www.ebi.ac.uk/eqtl/api/associations/%s?size=1000'%(rsid)
    response=requests.get(url)
    eqtls=response.json()
    try:
        genes_eqtls=[]
        eqtl_df=pd.DataFrame(columns=['variantid','p_value','log_pval','beta','alt','gene_id','tissue','study_id'])
        for ass in eqtls['_embedded']['associations'].keys():
            pval=eqtls['_embedded']['associations'][ass]['pvalue']
            nlog_pval=-np.log10(pval)
            beta=eqtls['_embedded']['associations'][ass]['beta']
            alt=eqtls['_embedded']['associations'][ass]['alt']
            geneid=eqtls['_embedded']['associations'][ass]['gene_id']
            tissue=eqtls['_embedded']['associations'][ass]['tissue']
            study=eqtls['_embedded']['associations'][ass]['study_id']
            eqtl_df.loc[ass]=[rsid,pval,nlog_pval,beta,alt,geneid,tissue,study]
            
        eqtl_df=eqtl_df.loc[eqtl_df.p_value<=p_value]
        
        eqtl_df=eqtl_df.reset_index(drop=True)
        if increase_index:
            eqtl_df.index+=1
    except Exception as er:
        print(er,eqtls)
        return None
    return eqtl_df






def get_genes(cr,start,stop,window=10000,pop='EUR',features=['gene'],mode='all'):
    
    """
    Retrieve genes in a window centered in a genomic position and compute the distance between the position and all the genes
    """
    winstart=start-window//2
    winend=stop+window//2
    str_features=';'.join(['feature='+x for x in features])
    http="https://rest.ensembl.org/overlap/region/human/%s:%s-%s?%s"%(cr,winstart,winend,str_features)
    risposta=requests.get(http,headers={ "Content-Type" : "application/json"}).json()
    if mode=='complete_data':
        return risposta
    elif mode=='all':
        elements={}
        for el in risposta:
            if el['biotype']=='protein_coding':
                try:
                    elements[el['external_name']]=int(el['start']-start)
                except:
                    pass
        return elements
    elif mode=='closest_forward':
        elements={}
        for el in risposta:
            if el['biotype']=='protein_coding':
                try:
                    elements[el['external_name']]=int(el['start']-start)
                except:
                    pass
        try:
            return min([(k,v) for (k,v) in elements.items() if v>0], key=lambda x:x[1])
        except:
            return 'no_genes_forward'
    elif mode=='closest_backward':
        elements={}
        for el in risposta:
            if el['biotype']=='protein_coding':
                try:
                    elements[el['external_name']]=int(el['start']-start)
                except:
                    pass
        try:
            return max([(k,v) for (k,v) in elements.items() if v<0], key=lambda x:x[1])
        except:
            return 'no_genes_backward'
    elif mode=='closest_overall':
        elements={}
        for el in risposta:
            if el['biotype']=='protein_coding':
                try:
                    elements[el['external_name']]=int(el['start']-start)
                except:
                    pass
        try:
            return min([(k,np.absolute(v)) for (k,v) in elements.items()], key=lambda x:x[1])
        except:
            return 'no_genes'


        
def ConvertVariantsForOT(ListOfVariants,source='variantid',target='rsid'):
    
    OT_url='https://api.genetics.opentargets.org/graphql'
    MappingDict={}
    if (source=='variantid') & (target=='rsid'):
        query="""{
               variantInfo(variantId:"%s"){
                   rsId
                   }
              }"""
        for variant in ListOfVariants:
            r = requests.post(OT_url, json={'query': query % (variant)})
            JsonResponse=r.json()
            MappingDict[variant]=JsonResponse['data']['variantInfo']['rsId']
        return list(map(MappingDict.get,ListOfVariants))

    elif (source=='rsid') & (target=='variantid'):
        query="""{
              search(queryString:"%s"){
                  variants{
                      id
                      }
                   }
              }
              """
        for variant in ListOfVariants:
            try:
                r = requests.post(OT_url, json={'query': query % (variant)})
                JsonResponse=r.json()
                MappingDict[variant]=JsonResponse['data']['search']['variants'][0]['id']
            except Exception as e:
                print(e, f"Couldn't Convert Variant {variant}")
        return list(map(MappingDict.get,ListOfVariants))


    
def OT_L2G(ListofVariants,score=0.1,output='genes'):
    query="""{
              genesForVariant(variantId:"%s"){
                overallScore
                gene{id}
              }
            }
            """
    OT_url='https://api.genetics.opentargets.org/graphql'
    
    results={}
    for variant in ListofVariants:
        r = requests.post(OT_url, json={'query': query % (variant)})
        r = r.json()
        ResultsForVariant=[]
        for data in r['data']['genesForVariant']:
            ResultsForVariant.append((data['gene']['id'],data['overallScore']))
        results[variant]=ResultsForVariant
    if output=='all':
        return results
    elif output=='GenScor':
        return {key:[value for value in values if value[1]>score] for (key,values) in results.items()}
    else:
        return list(set(sum([[value[0] for value in values if value[1]>score] for (key,values) in results.items()],[])))
    
            
            
    


