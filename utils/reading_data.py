from unstructured.partition.pdf import partition_pdf
import os
import re
from PyPDF2 import PdfReader
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from langchain_community.vectorstores import FAISS
from utils_functions import initialize_embedding_model
import faiss
import numpy as np

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def unstructured_pdf_reader(folder_path = "/mnt/c/Users/pc/Documents/complAI/Training materials for models/"):
    os.environ['EXTRACT_IMAGE_BLOCK_CROP_HORIZONTAL_PAD'] = '200'
    os.environ['EXTRACT_IMAGE_BLOCK_CROP_VERTICAL_PAD'] = '100'

    # Categorize by type
    tables = []
    texts = []
    for filename in os.listdir(folder_path):
        # Only process files that end with '.pdf'
        print(filename)
        if filename.endswith(".pdf"):
            raw_pdf_elements = partition_pdf(
                filename=folder_path+"/"+filename,
                strategy="hi_res",
                extract_images_in_pdf=True,
                infer_table_structure=True,
                chunking_strategy="by_title",
                max_characters=2000,
                new_after_n_chars=1900,
                combine_text_under_n_chars=1000,
                image_output_dir_path='/mnt/c/Users/pc/Documents/complAI/langchain_utils/',
            )
            
            for element in raw_pdf_elements:
                if "unstructured.documents.elements.Table" in str(type(element)):
                    tables.append(str(element))
                elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
                    texts.append(str(element))
        
    return texts, tables

def read_images_from_folder(folder_path='/mnt/c/Users/pc/Documents/complAI/figures/'):

    # List all files in the folder and filter for image file types
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]

    # Print the list of image files
    print(image_files)
    
def get_pdf_text_from_folder(folder_path, normalization=True):
    text = ""
    # List all files in the folder
    for filename in os.listdir(folder_path):
        # Only process files that end with '.pdf'
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)  # Get full path of the PDF
            pdf_reader = PdfReader(pdf_path)
            for page in pdf_reader.pages:
                if normalization:
                    text += re.sub(r'[^A-Za-z0-9\s.,?!\'“”:À-ÿ/()]+', '', page.extract_text())
                else:
                    text += page.extract_text()
    return text.lower()


def cluster_similar_embeddings_dbscan(embedding_model=None):
    embeddings = initialize_embedding_model()
    # Load the FAISS index
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # Extract embeddings and their corresponding texts
    embeddings = vectorstore.index.reconstruct_n(0, vectorstore.index.ntotal)
    texts = [doc.page_content for doc in vectorstore.docstore._dict.values()]

    # Convert embeddings to numpy array
    embeddings_array = np.array(embeddings)
    # Optional: Standardize the embeddings (important if using Euclidean distance)
    embeddings = StandardScaler().fit_transform(embeddings_array)

    # Step 2: Apply DBSCAN
    epsilon = 0.38  # Example parameter, needs tuning
    min_samples = 2  # Minimum number of points to form a cluster

    # DBSCAN clustering
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples, metric='cosine')
    labels = dbscan.fit_predict(embeddings)

    # Step 3: Post-processing to split clusters with more than 10 documents
    unique_labels = np.unique(labels)
    processed_labels = []

    for label in unique_labels:
        if label == -1:  # -1 is for outliers/noise
            processed_labels.extend([label] * np.sum(labels == label))
        else:
            # Get all documents in this cluster
            cluster_documents = np.where(labels == label)[0]
            
            # If cluster size > 10, split it using K-means or hierarchical clustering
            if len(cluster_documents) > 5:
                print(f"Cluster {label} has {len(cluster_documents)} documents, splitting...")
                
                # Example: Apply K-means to split the large cluster into smaller subclusters
                from sklearn.cluster import KMeans
                
                kmeans = KMeans(n_clusters=len(cluster_documents) // 5, random_state=42)
                sub_labels = kmeans.fit_predict(embeddings[cluster_documents])
                
                # Assign new labels to the documents in this cluster
                for i, doc_idx in enumerate(cluster_documents):
                    processed_labels.append(f"{label}_{sub_labels[i]}")
            else:
                # No need to split, keep the original label
                processed_labels.extend([label] * len(cluster_documents))

    # Convert processed labels into a numpy array
    processed_labels = np.array(processed_labels)

    i=0
    clusters_text = []
    for label in np.unique(processed_labels):
        print(f"\nCluster {label}:")
        if label != "-1":
            print("a")
            cluster_docs = np.where(processed_labels == label)[0]
            clusters_text.append("\n".join([texts[doc_idx] for doc_idx in cluster_docs]))
        else:
            cluster_docs = np.where(processed_labels == label)[0]
            clusters_text.extend([texts[doc_idx] for doc_idx in cluster_docs])
    
    return clusters_text

def clustering_embeddings_faiss(embedding_model=None):
    
    embeddings = initialize_embedding_model()
    # Load the FAISS index
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # Extract embeddings and their corresponding texts
    embeddings = vectorstore.index.reconstruct_n(0, vectorstore.index.ntotal)
    texts = [doc.page_content for doc in vectorstore.docstore._dict.values()]

    # Convert embeddings to numpy array
    embeddings_array = np.array(embeddings)

    # Initialize a FAISS index for nearest-neighbor search
    dimension = embeddings_array.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(embeddings_array)

    # Clustering with a max size of 10 per cluster
    max_cluster_size = 10
    clusters = []
    visited = set()

    for i in range(len(embeddings_array)):
        print(i)
        if i in visited:
            continue
        
        # Search for nearest neighbors
        _, neighbor_indices = faiss_index.search(embeddings_array[i:i+1], max_cluster_size)
        cluster = [idx for idx in neighbor_indices[0] if idx not in visited]
        
        # Add the cluster
        clusters.append(cluster)
        
        # Mark as visited
        visited.update(cluster)

    # Map clusters to texts
    text_clusters = [[texts[idx] for idx in cluster] for cluster in clusters]

    clusters_text = []
    for cluster_id, cluster_texts in enumerate(text_clusters):
        clusters_text.append("\n".join([text for text in cluster_texts]))
        
    return clusters_text