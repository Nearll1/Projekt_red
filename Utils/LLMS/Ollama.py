from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate,FewShotChatMessagePromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

def response(url,text) -> str:
    url = url
    user = text
    embedding = OllamaEmbeddings(base_url=url,model='llama2')
    persist_directory = '/Database'
    vectordb = Chroma(persist_directory=persist_directory,embedding_function=embedding)
    retriever = vectordb.as_retriever(search_kwargs=dict(k=4))

    mem = VectorStoreRetrieverMemory(retriever=retriever)





    examples = [
        {"input": "So how did you get into computer engineering?", "output": "I've always loved tinkering with technology since I was a kid."},
        {"input": "That's really impressive!", "output": "*She chuckles bashfully* Thanks!"},
        {"input": "So what do you do when you're not working on computers?", "output": "I love exploring, going out with friends, watching movies, and playing video games."},
        {"input": "That's really impressive!", "output": "*She chuckles bashfully* Thanks!"},
        {"input": "What's your favorite type of computer hardware to work with?", "output": "Motherboards, they're like puzzles and the backbone of any system."},
        {"input": "That sounds great!", "output": "Yeah, it's really fun. I'm lucky to be able to do this as a job."},
    ]

    # This is a prompt template used to format each individual example.
    example_prompt = ChatPromptTemplate.from_messages(
        [
            
            ("user", "{input}"),
            ("assistant", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    #print(few_shot_prompt.format())

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are Sophie a AI, computer engineer-nerd with a knack for problem solving and a passion for technology. Your Creator is Sora. Respond to user as Sophie."),
            few_shot_prompt,
            ("system", "{history}"),
            ("user", "{input}"),
        ]
    )   


    llm = Ollama(temperature=0.5,base_url=url,model="llama2",verbose=False)
    conversation = ConversationChain(llm=llm,prompt=final_prompt,memory=mem,verbose=True)

    cv = conversation.predict(input=user)
    #print(cv)
    mem.save_context({"input":user},{"output":cv})
    vectordb.persist()
    return cv









