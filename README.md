# PyDota
Pygame for yandex project in 2019 and coming soon... L.M.L

class Map:
  '''
    Инициализация и создание карты
  '''
  
class Level:
    '''
      По опыту выдаются какие-то способности, увеличивается регенирация - и тд.
      
    '''

class Unit:
    '''
      Создание персонажа с xp, mana
    '''
  
    class Hero(Unit, Level)
        ''' 
          Создание главного героя со спозобностями и левелом, и характеристиками
        '''

    class Bot_Hero(Unit, Level):
        '''
          Вражескиц герой
        '''

class Build:
    '''
      Инициализация здоровья, брони, и других характеристик у здания.
      
      должен быть пункт forbbiden - отвечает за уничтожение здания, можно уничтожить или нет.
    '''
    
    class Shop(Build):
        '''
            Инициализация товаров и тд
        '''
        
    сlass Tower(Build):
        '''
            Иницализация damage у здания
        '''
        
    class Gate(Build):
        '''
            Инициализация ворот прохода которые можн разрушить
        '''
        
     class Heal_build(Build):
        '''
          Инициализация здания которое может похилить героя
        '''
        
        
        