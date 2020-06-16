# survived_ast_lst = []
# survived_torp_lst = []
# len_ast_lst = len(self.__asteroids_lst)
# for i in range(len_ast_lst):
#     ast = self.__asteroids_lst[i]
#     if ast.has_intersection(self.__ship):
#         self.__screen.unregister_asteroid(ast)
#         self.__asteroids_lst.remove(ast)
#         self.__screen.show_message(LOST_LIFE_TITLE, LOST_LIFE_MSG)
#         self.__screen.remove_life()
#     else:
#         survived_ast_lst.append(ast)
# self.__asteroids_lst = survived_ast_lst
# len_ast_lst = len(self.__asteroids_lst)
# for j in range(len_ast_lst):
#     ast = self.__asteroids_lst[j]
#     len_torp_lst = len(self.__torpedos_lst)
#     for k in range(len_torp_lst):
#         torp = self.__torpedos_lst[k]
#         print(self.__asteroids_lst)
#         if ast.has_intersection(torp):
#             # self.__generate_baby_asteroids(ast, torp)
#             self.__screen.unregister_asteroid(ast)
#             self.__screen.unregister_torpedo(torp)
#             self.__asteroids_lst.remove(ast)
#             self.__torpedos_lst.remove(torp)
            #break
            #self.__add_score(ast.get_size())
#         else:
#             survived_ast_lst.append(ast)
#             survived_torp_lst.append(torp)
# self.__asteroids_lst = survived_ast_lst
# self.__torpedos_lst = survived_torp_lst