import openai
import pandas as pd
from openai.embeddings_utils import distances_from_embeddings


class CustomBot:
    def __init__(self, df, openai, context_column='context', has_embedding=False, file_name='custom_bot'):
        self.df = df
        self.openai = openai
        self.context_column = context_column
        self.has_embedding = has_embedding
        if not self.has_embedding:
            try:
                new_df = pd.read_csv(f'{file_name}.csv')
                # convert string to list
                new_df['embedding'] = new_df['embedding'].apply(
                    lambda x: eval(x))
                self.df['embedding'] = new_df['embedding']
                self.has_embedding = True
            except:
                self.df['embedding'] = self.df[self.context_column].apply(lambda x: openai.Embedding.create(input=x,
                                                                                                            engine='text-embedding-ada-002')['data'][0]['embedding'])
                self.has_embedding = True
                self.df.to_csv(f'{file_name}.csv')

    def create_context(self, question):
        q_embeddings = openai.Embedding.create(
            input=question, engine='text-embedding-ada-002')['data'][0]['embedding']
        self.df['distances'] = distances_from_embeddings(
            q_embeddings, self.df['embedding'].values, distance_metric='cosine')
        returns = []
        for i, row in self.df.sort_values('distances', ascending=True).head(5).iterrows():
            returns.append(row["context"])
        return "\n\n###\n\n".join(returns)

    def get_answer(
        self,
        # df,
        model="text-davinci-002",
        question="Am I allowed to publish model outputs to Twitter, without a human review?",
        debug=False,
        max_tokens=105,
        stop_sequence=None
    ):
        context = self.create_context(question)
        if debug:
            print(context)
        try:
            response = openai.Completion.create(
                model=model,
                prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
                max_tokens=max_tokens,
                temperature=0.5,
            )
            return response["choices"][0]["text"]
        except Exception as e:
            print(e)
            return "I don't know the answer to that."
