FROM minio/minio

COPY create-bucket.sh /usr/bin/create-bucket.sh
RUN chmod +x /usr/bin/create-bucket.sh

ENTRYPOINT ["/bin/sh", "-c", "minio server /var/lib/minio/data --console-address ':9002' & /usr/bin/create-bucket.sh && wait"]
