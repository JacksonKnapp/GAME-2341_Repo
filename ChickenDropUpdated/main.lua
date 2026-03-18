--game where animals fall from top player clicks
--before hit the bottom
--game ends when animal hits bottom

function love.load()
  chickenFace = love.graphics.newImage("chicken.png")
  backgroundImage = love.graphics.newImage("bg.png")
  powerUpImage = love.graphics.newImage("powerUp.png")
  PowerUp = 0
  Speed = 1

  math.randomseed(os.time())
  math.random(); math.random(); math.random()
  startx = {math.random(0, love.graphics.getWidth() - chickenFace:getWidth()), 
            math.random(0, love.graphics.getWidth() - chickenFace:getWidth()),  
            math.random(0, love.graphics.getWidth() - chickenFace:getWidth()),  
            math.random(0, love.graphics.getWidth() - chickenFace:getWidth()), 
            math.random(0, love.graphics.getWidth() - chickenFace:getWidth())}
  starty = {0 - math.random(chickenFace:getHeight(), chickenFace:getHeight() * 2),
            0 - math.random(chickenFace:getHeight(), chickenFace:getHeight() * 2),
            0 - math.random(chickenFace:getHeight(), chickenFace:getHeight() * 2),
            0 - math.random(chickenFace:getHeight(), chickenFace:getHeight() * 2),
            0 - math.random(chickenFace:getHeight(), chickenFace:getHeight() * 2)}
 -- assign random position for the powerup
  PowerUpX = math.random(powerUpImage:getWidth()/2, love.graphics.getWidth() - powerUpImage:getWidth())
  PowerUpY = math.random(powerUpImage:getHeight()/2, love.graphics.getHeight() - powerUpImage:getHeight())
end

-------------------------------------------------
--MOUSE PRESS
--1 = left, 2 = right, 3 = middle wheel
-------------------------------------------------
function love.mousepressed(x, y, button, istouch)
  if button == 1 then
    --print("left mouse clicked")
    for i, v in ipairs(startx) do
      --if the mouse x and y is within the boundary of a chicken picture
      if x >= startx[i] and x <= startx[i] + chickenFace:getWidth() and y >= starty[i] and y <= starty[i] + chickenFace:getHeight() then
        --print("in bounds")
        math.randomseed(os.time())
        math.random(); math.random(); math.random()
        --reset its y value (go back to the top)
        starty[i] = math.random(chickenFace:getHeight(), chickenFace:getHeight() * 2) * -1
      end
    end

    --if the mouse x and y is within the boundary of the powerup
    if x >= PowerUpX and x <= PowerUpX + powerUpImage:getWidth() and y >= PowerUpY and y <= PowerUpY + powerUpImage:getHeight() then
        Speed = 3
        PowerUp = 2 -- a value of 2 indicates that the power up has been used, this will stop it from being drawn
    end

  end
end

-------------------------------------------------
--UPDATE
-------------------------------------------------
function love.update(dt)

  for i, v in ipairs(starty) do
    --if chicken hits the bottom of the screen, lua quits (we lose)
    if starty[i] + chickenFace:getHeight() >= love.graphics.getHeight() then
      --print("over the edge")
      love.event.quit()
    end
    --chickens move down 
    starty[i] = starty[i] + 80 * Speed * dt
  end

  --test each frame whether to spawn a powerup. uses a weighted boolean. Only happens once
  if math.random() < .001 and PowerUp ~= 1 and PowerUp ~= 2 then
    PowerUp = 1
  end
end

-------------------------------------------------
--DRAW
-------------------------------------------------
function love.draw()
  love.graphics.draw(backgroundImage, 0, 0)
  --draw each chicken at their respective x and y
  for i, v in ipairs(startx) do
    love.graphics.draw(chickenFace, startx[i], starty[i])
  end
  -- draws powerup
  if PowerUp == 1 then
    love.graphics.draw(powerUpImage, PowerUpX, PowerUpY)
  end

end
