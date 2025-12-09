'''A python class used to model a power BI dashboard page

'''


import os


class _Page:
    '''A python class used to model a power BI dashboard page

    '''
    # pylint: disable=import-outside-toplevel
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-locals

    # Get everything else from the dashboard
    # Attribute delegation (inherit parent instance attributes)
    # pylint: disable=duplicate-code

    def __init__(self,
                 dashboard,
                 page_id=None):

        from powerbpy.dashboard import Dashboard



        if not isinstance(dashboard, Dashboard):
            raise TypeError("Pages must be attached to a Dashboard instance")


        # Define lists of objects that can be associated with a page
        self.background_images = []
        self.visuals = []



        self.dashboard = dashboard
        self.page_id = page_id

        # create a folder for the new page
        self.page_folder = os.path.join(self.dashboard.pages_folder, self.page_id)
        self.page_json_path = os.path.join(self.page_folder, "page.json")

        if not os.path.exists(self.page_folder):
            os.makedirs(self.page_folder)

        # Add subfolders for visuals and stuff
        self.visuals_folder = os.path.join(self.page_folder, "visuals")


    # pylint: disable=too-many-arguments
    def add_background_image(self,
                             img_path,
                             *,
                             alpha = 51,
                             scaling_method = "Fit"):


        '''Add a background image to a dashboard page
        Parameters
        ----------
        img_path: str
            The path to the image you want to add. (Can be a relative path because the image is copied to the report folder). Allowed image types are whatever PBI allows manually, so probably at least jpeg and png
        alpha: int
            The transparency of the background image. Must be a whole integer between 1 and 100.
        scaling_method: str
            The method used to scale the image available options include ["Fit", ]

        Notes
        ----
        Here's how you can add a background image to a page. To add the image, you'll need to provide the following required arguments:
            1. `img_path` - This is the path (relative or full) to the image you want to add to the dashboard

        There are two additional optional arguments:
            2. `alpha` - This is the image's transparency with 0 is fully transparent and 100 is full non-transparent (defaults to 100 )
            3. `scaling_method` - This tells Power BI how to scale the image (defaults to "Fit" which fits the image to the page)

        Here's some example code that adds a new background image to the Bee Colonies page:

        ```python
            page1.add_background_image(img_path = "examples/data/Taipei_skyline_at_sunset_20150607.jpg",
                   alpha = 51,
                   scaling_method = "Fit")
        ```
        And here's what the dashboard looks like, now that we've added a background image:
        ![Background Image Example](https://github.com/Russell-Shean/powerbpy/raw/main/docs/assets/images/background_image_example.png?raw=true "Background Image Example")
        '''

        # Local import avoids circular import at module load
        from powerbpy.background_image import _BackgroundImage

        background_image = _BackgroundImage(self,
                         img_path,
                         alpha,
                         scaling_method)

        self.background_images.append(background_image)
        return background_image

    # pylint: disable=too-many-arguments
    def add_chart(self,
                  *,
                  visual_id,
                 chart_type,
                 data_source,
                 chart_title,
                 x_axis_title,
                 y_axis_title,
                 x_axis_var,
                 y_axis_var,
                 y_axis_var_aggregation_type,
                 x_position,
                 y_position,
                 height,
                 width,
                 background_color="#FFFFFF",
                 background_color_alpha=None,
                 tab_order = -1001,
                 z_position = 6000,
                 parent_group_id = None,
                 alt_text="A chart"):

        '''This function adds a new chart to a page in a power BI dashboard report.
        Parameters
        ----------

        visual_id: str
            Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        chart_type: str
            The type of chart to build on the page. Known available types include: ["columnChart","barChart", "clusteredBarChart", ]
        data_source: str
            The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard.
        visual_title: str
            Give your chart an informative title!:D
        x_axis_title: str
            Text to display on the x axis
        y_axis_title: str
            Text to display on the y axis
        x_axis_var: str
            Column name of a column from data_source that you want to use for the x axis of the chart
        y_axis_var: str
            Column name of a column from data_source that you want to use for the y axis of the chart
        y_axis_var_aggregation_type: str
            Type of aggregation method you want to use to summarize y axis variable. Available options include" ["Sum", "Count", "Average"]
        x_position: int
            The x coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        height: int
            Height of chart on the page
        width: int
            Width of chart on the page
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
        '''

        from powerbpy.chart import _Chart

        chart = _Chart(self,
                      visual_id=visual_id,
                      chart_type=chart_type,
                 data_source=data_source,
                 visual_title=chart_title,
                 x_axis_title=x_axis_title,
                 y_axis_title=y_axis_title,
                 x_axis_var=x_axis_var,
                 y_axis_var=y_axis_var,
                 y_axis_var_aggregation_type=y_axis_var_aggregation_type,
                 x_position=x_position,
                 y_position=y_position,
                 height=height,
                 width=width,
                 tab_order=tab_order,
                 z_position=z_position,
                 parent_group_id=parent_group_id,
                 alt_text=alt_text,
                 background_color=background_color,
                 background_color_alpha=background_color_alpha)

        self.visuals.append(chart)
        return chart

    # pylint: disable=too-many-arguments
    def add_text_box(self,
                     *,
                 text,
                 visual_id,
                 height,
                 width,
                 x_position,
                 y_position,
                 z_position=6000,
                 tab_order=-1001,
                 parent_group_id=None,
                 alt_text="A text box",
                 font_weight = "bold",
                 font_size=32,
                 font_color="#000000",
                 background_color = None,
                 background_color_alpha=None):

        '''Add a text box to a page

        Parameters
        ----------
        text: str
            The text you want to display in the box
        visual_id: str
            Please choose a unique id to use to identify the text box. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        height:int
            Height of text box on the page
        width: int
            Width of text box on the page
        x_position: int
            The x coordinate of where you want to put the text box on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the text box on the page. Origin is page's top left corner.
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        font_weight: str
            This is an option to change the font's weight. Defaults to bold. Available options include: ["bold"]
        font_size: int
            The font size in pts. Must be a whole integer. Defaults to 32 pt
        font_color: str
            Hex code for the font color you'd like to use. Defaults to black (#000000)
        background_color: str
            Hex code for the background color of the text box. Defaults to None (transparent)
        parent_group_id: str
            This should be a valid id code for another power BI visual. If supplied the current visual will be nested inside the parent group.

        Notes
        -----
        This function creates a new text box on a page.
        '''

        from powerbpy.text_box import _TextBox

        text_box = _TextBox(self,
                 text=text,
                 visual_id=visual_id,
                 height=height,
                 width=width,
                 x_position=x_position,
                 y_position=y_position,
                 z_position=z_position,
                 tab_order=tab_order,
                 parent_group_id=parent_group_id,
                 alt_text=alt_text,
                 font_weight=font_weight,
                 font_size=font_size,
                 font_color=font_color,
                 background_color=background_color,
                 background_color_alpha=background_color_alpha)

        self.visuals.append(text_box)
        return text_box

    # pylint: disable=too-many-arguments
    def add_button(self,
                    *,
                 label,
                 visual_id,
                 height,
                 width,
                 x_position,
                 y_position,
                 z_position = 6000,
                 tab_order=-1001,
                 fill_color="#3086C3",
                 alpha=0,
                 url_link = None,
                 page_navigation_link = None,
                 alt_text="A button",
                 background_color = None,
                 background_color_alpha=None):

        '''Add a button to a page

        Parameters
        ----------
        label : str
            The text you want to display inside the button
        button_id: str
            Please choose a unique id to use to identify the button. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        height: int
            Height of text box on the page
        width: int
            Width of text box on the page
        x_position: int
            The x coordinate of where you want to put the text box on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the text box on the page. Origin is page's top left corner.
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        fill_color: str
            Hex code for the background (fill) color you'd like to use for the button. Defaults to blue (#3086C3)
        alpha: int
            The transparency of the fill color. Must be a whole integer between 1 and 100. Defaults to 0 (100% not transparent)
        url_link: str
            Optional argument. If provided, the button will navigate to this URL. Should be a full, not relative url
        page_navigation_link: str
            Optional argument. If provided the button will navigate to this page in the report. Must be a valid page_id already present in the report.

        Notes
        -----
        This function creates a new button on a page.
        '''

        from powerbpy.button import _Button

        button = _Button(self,
                 label=label,
                 visual_id=visual_id,
                 height=height,
                 width=width,
                 x_position=x_position,
                 y_position=y_position,
                 z_position =z_position,
                 tab_order=tab_order,
                 fill_color=fill_color,
                 alpha=alpha,
                 url_link = url_link,
                 page_navigation_link = page_navigation_link,
                 alt_text=alt_text,
                 background_color=background_color,
                 background_color_alpha=background_color_alpha)

        self.visuals.append(button)
        return button

    # pylint: disable=too-many-arguments
    def add_slicer(self,
                   *,
                  data_source,
               column_name,
               visual_id,
               height,
               width,
               x_position,
               y_position,
               z_position = 6000,
               tab_order=-1001,
               title = None,
               #text_align = "left",
               #font_weight = "bold",
               #font_size=32,
               #font_color="#000000",
               background_color = None,
               parent_group_id = None,
               alt_text= "A slicer",
                 background_color_alpha=None):

        '''Add a slicer to a page

        Parameters
        ----------
        data_source: str
            This is the name of the dataset that you want to use to populate the slicer with
        column_name: str
            This is the name of the measure (or variable) name you want to use to populate the slicer with
        visual_id: str
            Please choose a unique id to use to identify the slicer. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        height: int
            Height of slicer on the page
        width: int
            Width of slicer on the page
        x_position: int
            The x coordinate of where you want to put the slicer on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the slicer on the page. Origin is page's top left corner.
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        visual_title: str
            An optional title to add to the slicer.
        text_align: str
            How would you like the text aligned (available options: "left", "right", "center")
        font_weight: str
            This is an option to change the font's weight. Defaults to bold. Available options include: ["bold"]
        font_size: int
            The font size in pts. Must be a whole integer. Defaults to 32 pt
        font_color: str
            Hex code for the font color you'd like to use. Defaults to black (#000000)
        background_color: str
            Hex code for the background color of the slicer. Defaults to None (transparent)
        parent_group_id: str
            This should be a valid id code for another power BI visual. If supplied the current visual will be nested inside the parent group.

        Notes
        ------
        This function creates a new slicer on a page.
        '''

        from powerbpy.slicer import _Slicer

        slicer = _Slicer(self,
                data_source=data_source,
               column_name=column_name,
               visual_id=visual_id,
               height=height,
               width=width,
               x_position=x_position,
               y_position=y_position,
               z_position=z_position,
               tab_order=tab_order,
               visual_title=title,
               #text_align=text_align,
               #font_weight=font_weight,
               #font_size=font_size,
               #font_color=font_color,
               parent_group_id=parent_group_id,
               alt_text = alt_text,
                 background_color=background_color,
                 background_color_alpha=background_color_alpha)

        self.visuals.append(slicer)
        return slicer

    # pylint: disable=too-many-arguments
    def add_card(self,
                  *,
                 data_source,
             measure_name,
             visual_id,
             height,
             width,
             x_position,
             y_position,
             z_position = 6000,
             tab_order=-1001,
             card_title = None,
             #text_align = "left",
             font_weight = "bold",
             font_size=32,
             font_color="#000000",
             background_color = None,
             background_color_alpha = None,
             parent_group_id = None,
             alt_text="A card"):

        '''Add a card to a page

        Parameters
        ----------
        data_source: str
            This is the name of the dataset that you want to use to populate the card with
        measure_name: str
            This is the name of the measure (or variable) name you want to use to populate the card with
        visual_id: str
            Please choose a unique id to use to identify the card. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        height: int
            Height of card on the page
        width: int
            Width of card on the page
        x_position: int
            The x coordinate of where you want to put the card on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the card on the page. Origin is page's top left corner.
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        visual_title: int
            An optional title to add to the card.
        text_align: str
            How would you like the text aligned (available options: "left", "right", "center")
        font_weight: str
            This is an option to change the font's weight. Defaults to bold. Available options include: ["bold"]
        font_size: int
            The font size in pts. Must be a whole integer. Defaults to 32 pt
        font_color: str
            Hex code for the font color you'd like to use. Defaults to black (#000000)
        background_color: str
            Hex code for the background color of the card. Defaults to None (transparent)
        parent_group_id: str
            This should be a valid id code for another power BI visual. If supplied the current visual will be nested inside the parent group.

        Notes
        -----
        This function creates a new card on a page.
        '''



        from powerbpy.card import _Card

        card = _Card(self,
                 data_source=data_source,
             measure_name=measure_name,
             visual_id=visual_id,
             height=height,
             width=width,
             x_position=x_position,
             y_position=y_position,
             z_position = z_position,
             tab_order=tab_order,
             visual_title = card_title,
             font_weight = font_weight,
             font_size=font_size,
             font_color=font_color,
             background_color = background_color,
             background_color_alpha=background_color_alpha,
             parent_group_id = parent_group_id,
             alt_text=alt_text)

        self.visuals.append(card)
        return card

    # pylint: disable=too-many-arguments
    def add_shape_map(self,
                      *,
                   visual_id,
                  data_source,
                  shape_file_path,
                  map_title,
                  location_var,
                  color_var,
                  color_palette,
                  height,
                  width,
                  x_position,
                  y_position,
                  add_legend = True,
                  static_bin_breaks = None,
                  percentile_bin_breaks = None,
                  filtering_var = None,
                  z_position = 6000,
                  tab_order=-1001,
                  parent_group_id = None,
                 alt_text = "A shape map",
                 background_color = None,
                 background_color_alpha=None):

        '''Add a map to a page
        ![Example of a shape map created by the function](https://github.com/Russell-Shean/powerbpy/raw/main/docs/assets/images/page2.gif?raw=true "Example Shape Map")

        Parameters
        ----------
        visual_id: str
            Please choose a unique id to use to identify the map. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        data_source: str
            The name of the dataset you want to use to build the map. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard.
        shape_file_path: str
            A path to a shapefile that you want to use to build the map. This shape file will be added to the registered resources.
        map_title: str
            The title you want to put above the map.
        location_var: str
            The name of the column in data_source that you want to use for the location variable on the map
        color_var: str
            The name of the column in data_source that you want to use for the color variable on the map
        filtering_var: str
            Optional. The name of a column in data source that you want to use to filter the color variable on the map. This must be supplied if providing percentile_bin_breaks. If you want to use percentiles without filtering (ie on static data), you should calculate the percentiles yourself and pass them to static_bin_breaks. Do not provide both static_bin_breaks and a filtering_var.
        static_bin_breaks: list
            This should be a list of numbers that you want to use to create bins in your data. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. The function will create bins between the first and second number, second and third, third and fourth, etc. A filtering_var cannot be provided if static_bin_breaks is provided. Use percentile bin breaks instead.
        color_palatte: list
            A list of hex codes to use to color your data. There should be one fewer than the number of entries in static_bin_breaks
        add_legend: bool
            True or False, would you like to add the default legend? (By default legend, I mean this function's default, not the Power BI default)
        static_bin_breaks: list
            This should be a list of numbers that you want to use to create bins in your data. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. The function will create bins between the first and second number, second and third, third and fourth, etc.
        percentile_bin_breaks: list
            This should be a list of percentiles between 0 and 1 that you want to us to create bins in your data. If provided, a filtering_var must also be provided. This will create power BI measures that dynamically update when the data is filtered by things such as slicers. There should be one more entry in the list than the number of bins you want and therefore the number of colors passed to the color_palette argument. Here's an example use case: to create 5 equal sized bins pass this list: [0,0.2,0.4,0.6,0.8,1]
        height: int
            Height of map on the page
        width: int
            Width of map on the page
        x_position: int
            The x coordinate of where you want to put the map on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the map on the page. Origin is page's top left corner.
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)

        Notes
        -----
        This function creates a new cloropleth map on a page.
        '''

        from powerbpy.shape_map import _ShapeMap

        shape_map = _ShapeMap(self,
                   visual_id=visual_id,
                  data_source=data_source,
                  shape_file_path=shape_file_path,
                  map_title=map_title,
                  location_var=location_var,
                  color_var=color_var,
                  color_palette=color_palette,
                  height=height,
                  width=width,
                  x_position=x_position,
                  y_position=y_position,
                  add_legend = add_legend,
                  static_bin_breaks = static_bin_breaks,
                  percentile_bin_breaks = percentile_bin_breaks,
                  filtering_var = filtering_var,
                  z_position = z_position,
                  tab_order=tab_order,
                  parent_group_id = parent_group_id,
                 alt_text = alt_text,
                 background_color=background_color,
                 background_color_alpha=background_color_alpha)

        self.visuals.append(shape_map)
        return shape_map

    # pylint: disable=too-many-arguments
    def add_sanky_chart(self,
                        *,
                         visual_id,
                            data_source,
                            starting_var,
                            starting_var_values,
                            ending_var,
                            ending_var_values,
                            values_from_var,
                            x_position,
                            y_position,
                            height,
                            width,
                            chart_title,
                            link_colors=None,
                            alt_text="A sankey chart",
                            parent_group_id=None,
                            background_color="#FFFFFF",
                            background_color_alpha=None,
                            chart_title_font_size = 17,
                            #label_font_size = 20,
                            tab_order = -1001,
                            z_position = 6000):


        '''This function adds a new chart to a page in a power BI dashboard report.

        Parameters
        ----------
        chart_id: str
            Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        chart_type: str
            The type of chart to build on the page. Known available types include: ["columnChart","barChart", "clusteredBarChart", ]
        data_source: str
            The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard.
        starting_var: str
            Which variable from the data_source, do you want to use for the left side of the sanky chart?
        starting_var_values: list
            Which individual values do you want to use for the left side of the sanky chart? In general, this will probably mean all the unique values in the starting_var column. This function is setup to assume that you already know the structure of your data and can pass a list of unique values.
        ending_var: str
            Which variable from the data_source, do you want to use for the right side of the sanky chart?
        ending_var_values: list
            Which individual values do you want to use for the right side of the sanky chart? In general, this will probably mean all the unique values in the starting_var column. This function is setup to assume that you already know the structure of your data and can pass a list of unique values.
        values_from_var: str
            This is the variable that you want to count unique instances of as grouped by starting and ending variables. For now it only counts unique variables, but I'd like to add the option to provide a sum too
        chart_title: str
            Give your chart an informative title!:D
        alt_text: str
            Alternate text for the visualization can be provided as an argument. This is important for screen readers (accesibility) or if the visualization doesn't load properly.
        chart_title_font_size: int
            Font size for chart title
        label_font_size: int
            Font size for the labels on the various sanky nodes
        link_colors: list
            Here you can provide a list of Hex code colors for the connections between the different categories in the Sanky chart. In general this should be equal to the length of starting_var_values multiplied by the length of ending_var_values. If an argument is not provided the function assigns default colors.
        x_axis_var: str
            Column name of a column from data_source that you want to use for the x axis of the chart
        y_axis_var: str
            Column name of a column from data_source that you want to use for the y axis of the chart
        y_axis_var_aggregation_type: str
            Type of aggregation method you want to use to summarize y axis variable. Available options include" ["Sum", "Count", "Average"]
        x_position: int
            The x coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the chart on the page. Origin is page's top left corner.
        height: int
            Height of chart on the page
        width: int
            Width of chart on the page
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000

        '''



        from powerbpy.sanky_chart import _SankyChart

        sanky_chart = _SankyChart(self,
                            visual_id=visual_id,
                            data_source=data_source,
                            starting_var=starting_var,
                            starting_var_values=starting_var_values,
                            ending_var=ending_var,
                            ending_var_values=ending_var_values,
                            values_from_var=values_from_var,
                            x_position=x_position,
                            y_position=y_position,
                            height=height,
                            width=width,
                            chart_title=chart_title,
                            link_colors=link_colors,
                            alt_text=alt_text,
                            parent_group_id=parent_group_id,
                            background_color=background_color,
                            background_color_alpha=background_color_alpha,
                            chart_title_font_size = chart_title_font_size,
                            #label_font_size = label_font_size,
                            tab_order = tab_order,
                            z_position = z_position)

        self.visuals.append(sanky_chart)
        return sanky_chart

    # pylint: disable=too-many-arguments
    def add_table(self,
                  *,
                       visual_id,
                            data_source,
                            variables,
                            x_position,
                            y_position,
                            height,
                            width,
                            add_totals_row = False,
                            table_title = None,
                            table_title_font_size=None,
                            column_widths = None,
                            tab_order = -1001,
                            z_position = 6000,
                            alt_text="A table",
                            parent_group_id=None,
                            background_color="#FFFFFF",
                            background_color_alpha=None ):

        '''This function adds a new table to a page in a power BI dashboard report.
        Parameters
        ----------

        visual_id: str
            Please choose a unique id to use to identify the chart. PBI defaults to using a UUID, but it'd probably be easier if you choose your own id.
        data_source: str
            The name of the dataset you want to use to build the chart. This corresponds to the dataset_name field in the add data functions. You must have already loaded the data to the dashboard.
        variables: list
            The variables from the table that you want to include
        table_title: str
            Give your table an informative title!:D
        column_widths: dict
            Optional. Provide the width of columns. Provide the widths as a dictionary with column names as keys and widths as values.
        x_position: int
            The x coordinate of where you want to put the table on the page. Origin is page's top left corner.
        y_position: int
            The y coordinate of where you want to put the table on the page. Origin is page's top left corner.
        height: int
            Height of table on the page
        width: int
            Width of table on the page
        tab_order: int
            The order which the screen reader reads different elements on the page. Defaults to -1001 for now. (I need to do more to figure out what the numbers correpond to. It should also be possible to create a function to automatically order this left to right top to bottom by looping through all the visuals on a page and comparing their x and y positions)
        z_position: int
            The z index for the visual. (Larger number means more to the front, smaller number means more to the back). Defaults to 6000

        '''

        from powerbpy.table import _Table

        table = _Table(self,
                        visual_id=visual_id,
                            data_source=data_source,
                            variables=variables,
                            x_position=x_position,
                            y_position=y_position,
                            height=height,
                            width=width,
                            add_totals_row = add_totals_row,
                            table_title=table_title,
                            table_title_font_size=table_title_font_size,
                            column_widths=column_widths,
                            alt_text=alt_text,
                            parent_group_id=parent_group_id,
                            background_color=background_color,
                            background_color_alpha=background_color_alpha,
                            tab_order = tab_order,
                            z_position = z_position)

        self.visuals.append(table)
        return table
