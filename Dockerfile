FROM httpd:2.4

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc make pkg-config libgd-dev cpanminus emboss \
  && apt-get clean && rm -rf /var/lib/apt/lists/* \
  && cpanm CGI::Lite \
    Archive::Zip \
    Compress::Zlib \
    RTF::Parser \
    GD \
    GD::SVG \
    SVG \
    Statistics::Lite \
    Bio::Trace::ABIF

COPY ./conf/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./htdocs/ /usr/local/apache2/htdocs/
COPY ./cgi-bin/ /usr/local/apache2/cgi-bin/
