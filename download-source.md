# Download source files

The Univeristy of Chicago Booth School of Business makes data files available for academic use, along with PDF instruction manuals at this public location [Dominick's](https://www.chicagobooth.edu/research/kilts/research-data/dominicks).  This script will download the source movement files. From here, you will need to uncompress them and store them in a manner of your choosing. This research uses a script, [historic-data-prep](historic-data-prep.md), to store them on S3 -- all movement files in a single S3 folder.  The script works through some data quality issues; shapes the data and make it ready for training models and producing inference.
The following UNIX curl commands will move the ZIP archives from the Chicago Booth site for your "local storage" use.

In addition, a [PDF](https://www.chicagobooth.edu/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/dominicks-manual-and-codebook_kiltscenter) document was downloaded.  This contains important information and was used to develop the calendar dimension used in this research.

```
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wana_csv.zip --output wana.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wbat.zip --output wbat.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wber.zip --output wber.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wbjc.zip --output wbjc.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wcer.zip --output wcer.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wche.zip --output wche.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wcig.zip --output wcig.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wcra.zip --output wcra.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wcso.zip --output wcso.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wdid.zip --output wdid.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wfec.zip --output wfec.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wfrd.zip --output wfrd.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wfre.zip --output wfre.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wfrj.zip --output wfrj.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wfsf.zip --output wfsf.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wgro.zip --output wgro.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wlnd.zip --output wlnd.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/woat.zip --output woat.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wptw.zip --output wptw.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wsdr.zip --output wsdr.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wsha.zip --output wsha.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wsna.zip --output wsna.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wsoa.zip --output wsoa.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wtbr.zip --output wtbr.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wtna.zip --output wtna.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wtpa.zip --output wtpa.zip
curl https://www.chicagobooth.edu/research/kilts/research-data/-/media/enterprise/centers/kilts/datasets/dominicks-dataset/movement_csv-files/wtti.zip --output wtti.zip
```

