class EisenheimEng:
	"""
	EisenheimEng คือ
	ข้อมูลที่เกี่ยวข้องกับผู้สร้าง เพื่อใช้ในการเรียน Python
	ประกอบด้วย webpage in github.com
	งานอดิเรกคือ ดูรายการทำอาหารใน Youtube 
	
	Example:
	# --------------------
	eisen = EisenheimEng()
	eisen.show_name()
	eisen.show_youtube()
	eisen.about()
	eisen.ascii_chaiyo()
	# --------------------
	"""
	def __init__(self):
		self.name = 'Eisenheim L.'
		self.page = 'https://github.com/EisenheimA'

	def show_name(self):
		print(f'สวัสดีผมชื่อ {self.name}')

	def show_youtube(self):
		print('ช่อง Youtube ที่ชอบดู: https://www.youtube.com/@cookingwithdog')

	def about(self):
		text = """
	สวัสดีคร๊าบบ นี่คือ Package ที่แสดงข้อมูลเกี่ยวกับผู้เรียน Python
	ทำเพื่อประกอบการเรียน Python for Beginners from Zero EP10 คร๊าบบ
	"""
		print(text)
	def ascii_chaiyo(self):
		text = """
               *    *
   *         '       *       .  *   '     .           * *
                                                               '
       *                *'          *          *        '
   .           *               |               /
               '.         |    |      '       |   '     *
                \\*        \\   \\             /
       '         \\     '* |    |  *        |*                *  *
            *      `.      \\   |     *     /    *      '
  .                 \\      |  \\          /               *
     *'  *     '     \\     \\   '.       |
        -._            `                  /         *
  ' '      ``._   *                           '          .      '
   *          *\\*          * .   .      *
*  '        *    `-._                       .         _..:='        *
             .  '      *       *    *   .       _.:--'
          *           .     .     *         .-'         *
   .               '             . '   *           *         .
  *       ___.-=--..-._     *                '               '
                                  *       *
                *        _.'  .'       `.        '  *             *
     *              *_.-'   .'            `.               *
                   .'                       `._             *  '
   '       '                        .       .  `.     .
       .                      *                  `
               *        '             '                          .
     .                          *        .           *  *
             *        .                                    'Art by lgbeard
		"""
		print(text)

if __name__ == '__main__':
	eisen = EisenheimEng()
	eisen.show_name()
	eisen.show_youtube()
	print('-'*20)
	eisen.about()
	print('-'*20)
	eisen.ascii_chaiyo()

