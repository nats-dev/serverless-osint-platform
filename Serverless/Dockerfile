FROM public.ecr.aws/lambda/python:3.12

# Instalar git y herramientas de compilación
RUN dnf install -y git gcc python3-devel tar gzip && dnf clean all

# theHarvester
RUN git clone --depth 1 https://github.com/laramies/theHarvester.git ${LAMBDA_TASK_ROOT}/theHarvester && \
    cd ${LAMBDA_TASK_ROOT}/theHarvester && \
    pip install . && \
    rm -rf .git

# Código
COPY app.py ${LAMBDA_TASK_ROOT}

# Ejecutar
CMD [ "app.handler" ]