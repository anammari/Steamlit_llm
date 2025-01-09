1. **Run the container (initial command):**
   ```sh
   docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 -p 8501:8501 --name ollama ollama/ollama
   ```

2. **Enter the container:**
   ```sh
   docker exec -it ollama /bin/bash
   ```

3. **Start the container:**
   ```sh
   docker start ollama
   ```

4. **Stop the container:**
   ```sh
   docker stop ollama
   ```

5. **Run the Streamlit app with the `--server.address` option:**
   ```sh
   streamlit run your_app.py --server.address 0.0.0.0
   ```