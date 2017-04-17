FROM python:2.7 
USER root

# Environment var IDs
RUN pip install boto3
COPY ./pseudo.py /src/
COPY ./pseudo.sh /src/
RUN ["chmod", "+x", "/src/pseudo.sh"]
RUN mkdir /src/data /src/out
ENTRYPOINT ["/src/pseudo.sh"]
CMD ["panda.swerve"]
