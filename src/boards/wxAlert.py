from PIL import Image, ImageFont, ImageDraw, ImageSequence
from rgbmatrix import graphics
from time import sleep
from utils import center_text,get_file

class wxAlert:
    def __init__(self, data, matrix,sleepEvent):
        self.data = data
        self.layout4 = self.data.config.config.layout.get_board_layout('wx_alert')
        self.matrix = matrix
        self.pos = self.matrix.width
        self.sleepEvent = sleepEvent
        self.sleepEvent.clear()
        self.wxfont = data.config.layout.wxalert_font
        #Get size of summary text for looping 
        alert_info = self.matrix.draw_text(["50%", "50%"],self.data.wx_alerts[0],self.wxfont)
        #Set the width, add 3 to allow for text to scroll completely off screen
        self.alert_width = alert_info["size"][0] + 3

        self.scroll = self.data.config.weather_scroll_alert
        if not self.scroll:
            # Force to display the top and bottom titles on static display
            # This will be similar to the weather board alert display
            self.drawtitle = True
        else:
            self.drawtitle = self.data.config.weather_alert_title
        
        self.duration = self.data.config.weather_alert_duration
        
        
        self.wxDrawAlerts()
    
    def wxDrawAlerts(self):

        i = 0
        while True:
            self.matrix.clear()
            #offscreen_canvas = self.matrix.CreateFrameCanvas()

            if self.data.config.weather_units == "imperial":
                top_title = self.data.wx_alerts[4]
            else:
                top_title = "Weather"


            # Draw Alert boxes and numbers (warning,watch,advisory) for 64x32 board
            #self.matrix.draw.rectangle([60, 25, 64, 32], fill=(255,0,0)) # warning
            if self.data.wx_alerts[1] == "warning":
                self.matrix.draw.rectangle([0, 0, 64, 8], fill=(255,0,0)) # warning
                self.matrix.draw.rectangle([0, 24, 64, 32], fill=(255,0,0)) # warning
                
                if self.drawtitle:
                    if self.data.wx_alerts[0] == "Severe Thunderstorm":
                        self.data.wx_alerts[0] = "Svr T-Storm"
                    if self.data.wx_alerts[0] == "Freezing Rain":
                        self.data.wx_alerts[0] = "Frzn Rain"
                    if self.data.wx_alerts[0] == "Freezing Drizzle":
                        self.data.wx_alerts[0] = "Frzn Drzl"
                        
                    self.matrix.draw_text_layout(
                        self.layout4.title_top,
                        top_title
                    )  
                    self.matrix.draw_text_layout(
                        self.layout4.title_bottom,
                        "Warning"
                    )  

            elif self.data.wx_alerts[1] == "watch":
                if self.data.config.weather_units == "imperial":
                    self.matrix.draw.rectangle([0, 0, 64, 8], fill=(255,165,0)) # watch
                    self.matrix.draw.rectangle([0, 24, 64, 32], fill=(255,165,0)) # watch
                else:
                    self.matrix.draw.rectangle([0, 0, 64, 8], fill=(255,255,0)) # watch canada
                    self.matrix.draw.rectangle([0, 24, 64, 32], fill=(255,255,0)) # watch canada
                if self.drawtitle:   
                    self.matrix.draw_text_layout(
                        self.layout4.title_top,
                        top_title
                    )  
                    self.matrix.draw_text_layout(
                        self.layout4.title_bottom,
                        "Watch"
                    )  
            else:
                if self.data.wx_alerts[1] == "advisory":
                    if self.data.config.weather_units == "imperial":
                        self.matrix.draw.rectangle([0, 0, 64,8], fill=(255,255,0)) #advisory
                        self.matrix.draw.rectangle([0, 24, 64, 32], fill=(255,255,0)) #advisory
                    else:
                        self.matrix.draw.rectangle([0, 0, 64, 8], fill=(169,169,169)) #advisory canada
                        self.matrix.draw.rectangle([0, 24, 64, 32], fill=(169,169,169)) #advisory canada
                    
                    if self.drawtitle:
                        self.matrix.draw_text_layout(
                            self.layout4.title_top,
                            top_title
                        )  
                        self.matrix.draw_text_layout(
                            self.layout4.title_bottom,
                            "Advisory"
                        )  
            
            if self.scroll:
                self.matrix.draw_text([self.pos,9],self.data.wx_alerts[0],self.wxfont,fill=(255,255,255))
                

                if self.alert_width > self.pos:
                    self.pos -= 1
                    if self.pos + self.alert_width == 0:
                        break
                self.matrix.render()
                sleep(0.1)
            else:
                self.matrix.draw_text_layout(
                    self.layout4.warning,
                    self.data.wx_alerts[0]
                )
                self.matrix.draw_text_layout(
                    self.layout4.warning_date,
                    self.data.wx_alerts[2]
                )
                self.matrix.render()
                sleep(1)
                i+=1
                if i==self.duration:
                    break
            
            if self.data.network_issues and not self.data.config.clock_hide_indicators:
                self.matrix.network_issue_indicator()
            
            if self.data.newUpdate and not self.data.config.clock_hide_indicators:
                self.matrix.update_indicator()
            