UPDATE `ebay_stores` set `item_description_template` = '<!-- Zinc EPID: {{ asin }} -->
<font size="6" color="blue">Welcome To BJWorld!</font>
<BR><BR>
<B><font size="4">{{ title }}</font></B>
<BR>
<BR><BR>
<B>Product Description</B>
<BR><BR>
{{ description }}
<BR><BR>
<B>Product Features</B>
<BR><BR>
{{ features }}' WHERE `id` = 3;