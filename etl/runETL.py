# =========================
# RUN ETL PIPELINE
# =========================

from process import run_processing
from storeInSupabase import store_in_supabase

def main():

    chunks, embeddings = run_processing()

    store_in_supabase(chunks, embeddings)

    print("🎉 ETL COMPLETED!")

if __name__ == "__main__":
    main()