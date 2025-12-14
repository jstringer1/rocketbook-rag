FROM ollama/ollama:latest AS builder

RUN ollama serve & \
    OLLAMA_PID=$! && \
    sleep 10 && \
    ollama pull llama3.1:8b && \
    kill $OLLAMA_PID

FROM ollama/ollama:latest

COPY --from=builder /root/.ollama /root/.ollama

EXPOSE 11434

ENTRYPOINT ["ollama"]
CMD ["serve"]

