html = '''
<select id="sort" name="sort">
                <option value="Lowest to Highest Price">Lowest to Highest Price</option>
                <option value="Highest to Lowest Price">Highest to Lowest Price</option>
                <option value="Alphabetical Order">Alphabetical Order</option>
                <option value="Reversed Alphabetical Order">Reversed Alphabetical Order</option>
              </select>
              <br>
              <br>
              <p class="filtersort_by_title">Filter By:</p>
              <br>
              <label for="status">Availability:</label>
              <br>
              <select id="status" name="status">
                <option value=" ">No Preference</option>
                <option value="In Store Only">In Store Only</option>
                <option value="Available Online">Available Online</option>
              </select>
              <br>
              <label for="status">Brand:</label>
              <br>
              <select id="brand" name="brand">
                <option value=" ">No Preference</option>
                <option value="Scott">Scott</option>
                <option value="Charmin">Charmin</option>
                <option value="Cottonelle">Cottonelle</option>
                <option value="Just The Basics">Just The Basics</option>
                <option value="Total Home">Total Home</option>
                <option value="Berkley Jensen">Berkley Jensen</option>
                <option value="Kamenstein">Kamenstein</option>
                <option value="Vanity Fair">Vanity Fair</option>
                <option value="Angel Soft">Angel Soft</option>
                <option value="Great Value">Great Value</option>
                <option value="Seventh Generation">Seventh Generation</option>
              </select>
'''
def selected_option(field, key, html):
    select_loc = html.find('<select id="' + field + '" ' +'name="' + field + '">')
    option_loc = html[select_loc:].find('value="'+ key + '"') + select_loc
    return html[:option_loc] + ' selected ' + html[option_loc:]

print(selected_option('brand', "Berkley Jensen", html))