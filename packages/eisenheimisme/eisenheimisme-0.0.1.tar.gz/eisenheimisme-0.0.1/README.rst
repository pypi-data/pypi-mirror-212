Package นี้ เป็นการสร้าง Library Python เพื่อ Upload ขึ้น PyPi.org ตอน “pip install (MyName)”
=============================================================================================

PyPi: https://pypi.org/project/eisenheimisme/

EisenheimEng คือ ข้อมูลที่เกี่ยวข้องกับผู้สร้าง เพื่อใช้ในการเรียน
Python ประกอบด้วย webpage ของผู้สร้าง in github.com งานอดิเรกคือ
ดูรายการทำอาหารใน Youtube

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install eisenheimisme

วิธีใช้งานแพ็คเพจนี้
~~~~~~~~~~~~~~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

.. code:: python

   from eisenheimisme import EisenheimEng

   eisen = EisenheimEng() # ประกาศชื่อ class
   eisen.show_name() # แสดงชื่อ
   eisen.show_youtube() # แสดงช่อง Youtube ที่ชอบดู
   eisen.about() # เกี่ยวกับ Eisen
   eisen.ascii_chaiyo()# แสดงภาพพลุ เพื่อยินดีกับผู้เข้าชม

พัฒนาโดย: Eisenheim L. github.com: https://github.com/EisenheimA
