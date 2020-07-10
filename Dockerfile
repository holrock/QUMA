FROM httpd:2.4

RUN apt-get update && apt-get install -y --no-install-recommends \
  make cpanminus emboss \
  && apt-get clean && rm -rf /var/lib/apt/lists/* \
  && cpanm CGI::Lite Archive::Zip RTF::Parser Bio::Trace::ABIF Statistics::Lite

COPY ./conf/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./htdocs/ /usr/local/apache2/htdocs/
COPY ./cgi-bin/ /usr/local/apache2/cgi-bin/
