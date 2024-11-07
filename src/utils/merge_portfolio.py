def merge_portfolios(portafolio, portafolio_update):
    # Convertimos portafolio a un diccionario para un acceso más fácil
    portafolio_dict = {entry['user_id'].strip(): entry for entry in portafolio}
    
    # Iterar sobre cada usuario y sus portafolios en portafolio_update
    for user, user_portfolio in portafolio_update.items():
        if user in portafolio_dict:
            # Si el usuario existe, obtenemos su portafolio existente y actualizamos
            existing_portfolio = portafolio_dict[user]['holdings']
            for stock, amount in user_portfolio.holdings.items():
                existing_portfolio[stock] = existing_portfolio.get(stock, 0)
        else:
            # Si el usuario no existe, simplemente añadimos el nuevo portafolio
            portafolio_dict[user] = {'user_id': user, 'holdings': dict(user_portfolio.holdings)}

    # Convertir el diccionario actualizado nuevamente a una lista para el formato original
    return list(portafolio_dict.values())
