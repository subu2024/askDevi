# image download


# The MIT License (MIT)
#
# Copyright (c) Lumos AI LLC
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Subu Sangameswar


import urllib.request
import pandas as pd
import pandas as pd
import os as o

#SarojfabircInventory022122
csv_file_to_read = 'Consolidated_Data_052022.csv'
save_as_csv = 'Consolidated_Data_052022_updated.csv'
save_as_html = 'Consolidated_Data_052022_updated.html'
file_name_prefix_for_images = './images/ask_devi_images_'




def make_clickable(path):
    # returns the final component of a url
    f_url = o.path.basename(path)

    # convert the url into link
    return '<a href="{}">{}</a>'.format(path, f_url)

def make_visible(path):
    # returns the final component of a url
    f_url = o.path.basename(path)
      
    # convert the url into link
    return '<img src="{}" width="50" height="50">{}</>'.format(path, f_url)


def read_csv():

   df = pd.read_csv(csv_file_to_read)

   # get only specific columns
   #df_selected=df['Acct','Vendor','Material','Material_Description','Image','ImageNum']
   # remove blank rows and rename the columns
   df_filtered = df[df['Vendor'].notnull()]
   df_filtered.rename(columns={'Acct': 'ID', 'Material_Description': 'desc' }, inplace=True)

   return df_filtered


def save_to_csv(df):

    # rename columns
    #df_filtered.rename(columns={'recipe_name': 'title', 'ingredients': 'desc'}, inplace=True)
    df.to_csv(save_as_csv, index=True)


def save_to_html():
   
   df = pd.read_csv(save_as_csv)

   # duplicate the image column
   df['img_url'] = df['Image Src']

   df['img_url'] = df['img_url'].apply(make_clickable)

   df = df.style.format({'Image Src': make_visible})

   df.to_html(save_as_html, render_links=True, escape=False)


def process_images(df):

   #download the image and add a new filename
   image_name = []
   file_found =[]


   for ind in df.index:
      #imgURL = df['recipe_urls'][ind]
      imgURL = df['Image'][ind]
      file_name = file_name_prefix_for_images + str(ind) + ".jpg"
      #print(file_name, imgURL)
      image_name.append(file_name)
      print('processing file:', file_name)
      try:
         # do not download files becuase this is a huge file
         urllib.request.urlretrieve(imgURL, file_name)
         file_found.append("y")
      except:
         file_found.append("n")


   #print(image_name)
   df["Image Src"] = image_name
   df["found"] = file_found 
   
   #get only the rows which has valid images
   df_filtered_final = df[df['found'] == "y"]

   return df_filtered_final



def main():
   df = read_csv()
   df_final = process_images(df)
   #print(df_final)
   save_to_csv(df_final)
   save_to_html()


# letting python know explicitly where to start
if __name__ == '__main__':
    main()