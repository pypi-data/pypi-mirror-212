
class Template:

  template_model = dict(

    Birthyear = dict(
      process_type = "http://purl.obolibrary.org/obo/NCIT_C142470",
      output_type = "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type = "http://purl.obolibrary.org/obo/NCIT_C83164",
      value_datatype = "xsd:integer",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Birthdate = dict(
      process_type = "http://purl.obolibrary.org/obo/NCIT_C142470",
      output_type = "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type = "http://purl.obolibrary.org/obo/NCIT_C68615",
      value_datatype = "xsd:date",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Deathdate = dict( 
      process_type= "http://purl.obolibrary.org/obo/NCIT_C142470",
      output_type= "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type = "http://purl.obolibrary.org/obo/NCIT_C70810",
      value_datatype = "xsd:date",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    First_visit = dict(
      process_type = "http://purl.obolibrary.org/obo/NCIT_C142470",
      output_type = "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type = "http://purl.obolibrary.org/obo/NCIT_C164021",
      value_datatype = "xsd:date",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Sex = dict( 
      process_type = "http://purl.obolibrary.org/obo/NCIT_C142470",
      output_type = "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type2 = "http://purl.obolibrary.org/obo/NCIT_C28421",
      value_datatype = "xsd:string",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),


    Status = dict(
      process_type = "http://purl.obolibrary.org/obo/NCIT_C142470",
      output_type = "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type2 = "http://purl.obolibrary.org/obo/NCIT_C166244",
      value_datatype = "xsd:string",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Diagnosis = dict(
      process_type= "http://purl.obolibrary.org/obo/NCIT_C15220",
      output_type= "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type2= "http://purl.obolibrary.org/obo/NCIT_C2991",
      value_datatype = "xsd:string",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Symptoms = dict(
      process_type= "http://purl.obolibrary.org/obo/NCIT_C15220",
      output_type = "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type2= "http://purl.obolibrary.org/obo/NCIT_C100104",
      value_datatype = "xsd:string",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Genetic = dict(
      process_type= "http://purl.obolibrary.org/obo/NCIT_C15709",
      output_type= "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type= "http://purl.obolibrary.org/obo/NCIT_C103223",
      attribute_id_type = "http://purl.obolibrary.org/obo/NCIT_C45766",
      value_datatype = "xsd:string",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Consent_contacted = dict(
      process_type= "http://purl.obolibrary.org/obo/OBI_0000810",
      output_type = "http://purl.obolibrary.org/obo/OBIB_0000488",
      attribute_type= "http://purl.obolibrary.org/obo/NCIT_C25460",
      value_datatype = "xsd:string",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Consent_used = dict(
      process_type= "http://purl.obolibrary.org/obo/OBI_0000810",
      output_type = "http://purl.obolibrary.org/obo/DUO_0000001",
      attribute_type= "http://purl.obolibrary.org/obo/NCIT_C25460",
      value_datatype = "xsd:string",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Biobank = dict(
      process_type= "http://purl.obolibrary.org/obo/OMIABIS_0000061",
      output_type= "http://purl.obolibrary.org/obo/NCIT_C115570",
      attribute_type= "http://purl.obolibrary.org/obo/NCIT_C25429",
      value_datatype = "xsd:string",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Disability = dict(
      process_type = None,
      output_type = "http://purl.obolibrary.org/obo/NCIT_C70856",
      attribute_type = "http://purl.obolibrary.org/obo/NCIT_C21007",
      value_datatype = "xsd:float",
      startdate = None,
      enddate = None,
      pid = None,
      context_id = None
    ),

    Body_measurement = dict(
      process_type = "http://purl.obolibrary.org/obo/NCIT_C142470" ,
      output_type=  "http://purl.obolibrary.org/obo/NCIT_C70856" ,
      value_datatype= "xsd:float" ,
      startdate= None ,
      enddate= None ,
      comments= None ,
      pid= None ,
      context_id= None 
    ),


    Lab_measurement = dict(
      process_type = "http://purl.obolibrary.org/obo/NCIT_C25294" ,
      output_type = "http://purl.obolibrary.org/obo/NCIT_C70856" ,
      value_datatype= "xsd:float" ,
      startdate= None ,
      enddate= None ,
      comments= None ,
      pid= None ,
      context_id= None 
    ),


    Imaging = dict(
      process_type = None ,
      output_type =  "http://purl.obolibrary.org/obo/NCIT_C70856" ,
      attribute_type = "http://purl.obolibrary.org/obo/NCIT_C176708",
      attribute_id_type = "http://purl.obolibrary.org/obo/NCIT_C81289",
      value_datatype = "xsd:string" ,
      startdate= None ,
      enddate= None ,
      comments= None ,
      pid = None ,
      context_id= None 
    ),


    Intervention = dict(
      value_datatype = "xsd:string" ,
      startdate= None ,
      enddate= None ,
      comments= None ,
      pid= None ,
      context_id= None 
    ),


    Clinical_trial = dict(
      process_type = "http://purl.obolibrary.org/obo/NCIT_C71104" ,
      output_type=  "http://purl.obolibrary.org/obo/NCIT_C115575" ,
      attribute_type2 = "http://purl.obolibrary.org/obo/NCIT_C2991" ,
      agent_type = "http://purl.obolibrary.org/obo/NCIT_C16696" ,
      value_datatype= "xsd:string",
      startdate= None ,
      enddate= None ,
      comments= None ,
      pid= None ,
      context_id= None
    ),


    Medications = dict(
      process_type = "http://purl.obolibrary.org/obo/NCIT_C25409",
      output_type =  "http://purl.obolibrary.org/obo/NCIT_C459" ,
      agent_type = "http://purl.obolibrary.org/obo/NCIT_C177929",
      value_datatype= "xsd:float",
      startdate= None ,
      enddate = None ,
      comments = None ,
      pid = None ,
      context_id = None 
    )


  )

