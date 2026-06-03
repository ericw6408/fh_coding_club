class Character:
    def __init__(self,image,x,y):
        self.image = image
        self.pos = [x,y]
        self.velocity = [0,0]
        self.size = self.image.get_size()
    
    def move_x(self,dx):
        self.pos[0] += dx
    
    def move_y(self,dy):
        self.pos[1] += dy
    
    def move_by(self,velocity):
        self.move_x(velocity[0])
        self.move_y(velocity[1])

    def set_xpos(self,x):
        self.pos[0] = x
    
    def set_ypos(self,y):
        self.pos[1] = y
        
    def set_pos(self,pos):
        self.set_xpos(pos[0])
        self.set_ypos(pos[1])
    

    def change_x_vel(self,dv_x):
        self.velocity[0] += dv_x
    
    def change_y_vel(self,dv_y):
        self.velocity[1] += dv_y

    def change_velocity(self,dv):
        self.change_x_vel(dv[0])
        self.change_y_vel(dv[1])

    def set_xvel(self,x_vel):
        self.velocity[0] = x_vel
    
    def set_yvel(self,y_vel):
        self.velocity[1] = y_vel

    def set_velocity(self,v):
        self.set_xvel(v[0])
        self.set_yvel(v[1])

    def tick(self):
        self.move_by(self.velocity)


    def draw_self(self,surface):
        surface.blit(self.image,self.pos)
