class EncodeTextSource:
  def __init__(self):
    self.is_loadtokenizers=False



  def tokenize_and_generate_embeddings_descriptions(self,description):
    if not self.is_loadtokenizers:
      raise ValueError("tokenizers dont load")
    # Tokenize input description and move tokens to GPU
    tokens = self.beart_tokenizer.encode_plus(description, return_tensors="pt", truncation=True)
    tokens = {key: value.to(device) for key, value in tokens.items()}
    # Generate embeddings
    with torch.no_grad():
        outputs = self.beart_model(**tokens)
    # Extract embeddings for all tokens
    desc_embeddings = outputs.last_hidden_state.cpu().numpy()
    return desc_embeddings

  def tokenize_and_generate_embeddings_codes(self,code):
    if not self.is_loadtokenizers:
      raise ValueError("tokenizers dont load")
    # Tokenize input code and move tokens to GPU
    tokens = self.codebeart_tokenizer.encode_plus(code, return_tensors="pt", truncation=True)
    tokens = {key: value.to(device) for key, value in tokens.items()}
    # Generate embeddings
    with torch.no_grad():
        outputs = self.codebeart_model(**tokens)
    # Extract embeddings for all tokens
    code_embeddings = outputs.last_hidden_state.cpu().numpy()

    return code_embeddings


  def tokenize_and_generate_embeddings_graphcodes(self,code):
    if not self.is_loadtokenizers:
      raise ValueError("tokenizers dont load")
    # Tokenize input code and move tokens to GPU
    tokens = self.graphcodebert_tokenizer.encode_plus(code, return_tensors="pt", truncation=True)
    tokens = {key: value.to(device) for key, value in tokens.items()}
    # Generate embeddings
    with torch.no_grad():
        outputs = self.graphcodebert_model(**tokens)
    # Extract embeddings for all tokens
    code_embeddings = outputs.last_hidden_state.cpu().numpy()
    return code_embeddings

  def load_beart_tokenizer(self):
    # Verificar si la GPU está disponible
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Cargar el tokenizer y el modelo en la GPU si está disponible
    model_name = "bert-base-uncased"
    self.beart_model = BertModel.from_pretrained(model_name)
    self.beart_tokenizer = BertTokenizer.from_pretrained(model_name)
    self.beart_model.to(device)

  def load_graphcodebert_tokenizer(self):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    self.graphcodebert_tokenizer = AutoTokenizer.from_pretrained("microsoft/graphcodebert-base")
    self.graphcodebert_model = AutoModel.from_pretrained("microsoft/graphcodebert-base")
    self.graphcodebert_model.to(device)


  def load_codebert_tokenizer(self):
    # Verificar si la GPU está disponible
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Cargar el tokenizer y el modelo en la GPU si está disponible
    self.codebeart_tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    self.codebeart_model = RobertaModel.from_pretrained("microsoft/codebert-base")
    self.codebeart_model.to(device)

  def start_tokenizer(self):
    self.load_beart_tokenizer()
    #self.load_codebert_tokenizer()
    self.load_graphcodebert_tokenizer()
    self.is_loadtokenizers=True
