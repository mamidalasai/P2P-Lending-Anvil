from ._anvil_designer import edit_formTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class edit_form(edit_formTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.data = tables.app_tables.fin_product_details.search()

        # Fetch data from product_group table and populate the name dropdown
        product_group_options = app_tables.fin_product_group.search()
        self.name.items = [option['name'] for option in product_group_options]

        # Fetch data from product_group table and populate the name dropdown
        product_group_options = app_tables.fin_product_categories.search()
        self.product_category.items = [option['name_categories'] for option in product_group_options]

        self.id_list = []
        self.product_name_lst = []
        self.name_list = []
        self.product_categorys = []
        self.discri_list = []
        self.profee_list = []
        self.extfee_list = []
        self.foreclosure_type_list = []
        self.fore_fee = []
        self.extension_allowed_list = []
        self.type_list = []
        self.intr_type = []
        self.roi_list = []
        self.min_amount_list = []
        self.max_amount_list = []
        self.min_tenure_list = []
        self.max_tenure_list = []
        self.emi_payment_list = []
        self.lapsed_lst = []
        self.default_lst = []
        self.npa_lst = []
        self.min_month_list = []
        self.disc_coupans_list = []

        a = -1
        for i in self.data:
            a += 1
            self.id_list.append(i['product_id'])
            self.product_name_lst.append(i['product_name'])
            self.name_list.append(i['product_group'])
            self.discri_list.append(i['product_discription'])
            self.product_categorys.append(i['product_categories'])
            self.profee_list.append(i['processing_fee'])
            self.extfee_list.append(i['extension_fee'])
            self.foreclosure_type_list.append(i['foreclose_type'])
            self.fore_fee.append(i['foreclosure_fee'])
            self.extension_allowed_list.append(i['extension_allowed'])
            self.type_list.append(i['membership_type'])
            self.intr_type.append(i['interest_type'])
            self.roi_list.append(i['roi'])
            self.max_amount_list.append(i['max_amount'])
            self.min_amount_list.append(i['min_amount'])
            self.min_tenure_list.append(i['min_tenure'])
            self.max_tenure_list.append(i['max_tenure'])
            self.emi_payment_list.append(i['emi_payment'])
            self.lapsed_lst.append(i['lapsed_fee'])
            self.default_lst.append(i['default_fee'])
            self.npa_lst.append(i['npa'])
            self.min_month_list.append(i['min_months'])
            self.disc_coupans_list.append(i['discount_coupons'])

        if a == -1:
            alert("No Data Available Here!!")
        else:
            if self.id_list:
                self.label_1.text = str(self.id_list[-1])

            if self.product_name_lst:
                self.product_name.text = self.product_name_lst[-1]

            if self.name_list:
                self.name.selected_value = self.name_list[-1]

            if self.discri_list:
                self.discri_list = str(self.discri_list[-1])

            if self.product_categorys:
                self.product_category.selected_value = self.product_categorys[-1]

            if self.profee_list:
                self.text_box_3.text = str(self.profee_list[-1])

            if self.extfee_list:
                self.text_box_4.text = str(self.extfee_list[-1])

            if self.foreclosure_type_list:
                self.foreclose_type.selected_value = self.foreclosure_type_list[-1]

            if self.fore_fee:
                self.foreclosure_fee.text = str(self.fore_fee[-1])

            if self.extension_allowed_list:
                self.extension_allowed.selected_value = str(self.extension_allowed_list[-1])  # or .selected_value?

            if self.type_list:
                self.drop_down_2.selected_value = self.type_list[-1]

            if self.intr_type:
                selected_interest_type = str(self.intr_type[-1])
                if selected_interest_type == "Fixed":
                    self.radio_button_1.selected = True
                    self.radio_button_2.selected = False
                    self.radio_button_3.enabled = False
                    self.radio_button_4.enabled = False
                    self.radio_button_3.selected = True  
                    self.radio_button_4.selected = False 
                    self.text_area_1.enabled = False
                    self.product_name.enabled = False
                    self.min_amount.enabled = False
                    self.drop_down_2.enabled = False
                    self.max_amount.enabled = False
                    self.min_tenure.enabled = False
                    self.max_tenure.enabled = False
                    self.roi.enabled = False
                    self.foreclosure_fee.enabled = False
                    self.foreclose_type.enabled = False
                    self.extension_allowed.enabled = False
                    self.min_months.enabled = False
                    self.name.enabled = False
                    self.product_category.enabled = False
                    self.text_box_3.enabled = False
                    self.text_box_4.enabled = False
                    self.check_box_1.enabled = False
                    self.check_box_2.enabled = False
                    self.lapsed.enabled = False
                    self.default.enabled = False
                    self.npa.enabled = False
                    self.radio_button_3.selected = False
                    self.radio_button_4.selected = False
                elif selected_interest_type == "Variable":
                    self.radio_button_1.selected = False
                    self.radio_button_2.selected = True
                    self.radio_button_3.enabled = False
                    self.radio_button_4.enabled = False
                    self.text_area_1.enabled = False
                    self.min_amount.enabled = False
                    self.roi.enabled = True
                    self.drop_down_2.enabled = False
                    self.max_amount.enabled = False
                    self.min_tenure.enabled = False
                    self.max_tenure.enabled = False
                    self.foreclose_type.enabled = False
                    self.extension_allowed.enabled = False
                    self.min_months.enabled = False
                    self.name.enabled = False
                    self.product_name.enabled = False
                    self.product_category.enabled = False
                    self.text_box_3.enabled = False
                    self.foreclosure_fee.enabled = False
                    self.text_box_4.enabled = False
                    self.check_box_1.enabled = False
                    self.check_box_2.enabled = False
                    self.lapsed.enabled = False
                    self.default.enabled = False
                    self.npa.enabled = False
                    self.radio_button_3.selected = False
                    self.radio_button_4.selected = False
                else:
                    print(f"Unexpected interest type: {selected_interest_type}")

            else:
                # Assuming "Variable" when intr_type is not available
                self.radio_button_1.selected = False
                self.radio_button_2.selected = False
                self.radio_button_3.enabled = False
                self.radio_button_4.enabled = False


            if self.roi_list:
                self.roi.text = str(self.roi_list[-1])

            if self.min_amount_list:
                self.min_amount.text = str(self.min_amount_list[-1])

            if self.max_amount_list:
                self.max_amount.text = str(self.max_amount_list[-1])

            if self.min_tenure_list:
                self.min_tenure.text = str(self.min_tenure_list[-1])

            if self.max_tenure_list:
                self.max_tenure.text = str(self.max_tenure_list[-1])

            if self.emi_payment_list:
                self.checkbox_values = [
                    self.check_box_1.checked,
                    self.check_box_2.checked,
                    self.check_box_3.checked,
                    self.check_box_4.checked
                ]
            if self.emi_payment_list:
                checkbox_values = self.emi_payment_list[-1]
                self.check_box_1.checked = checkbox_values[0]
                self.check_box_2.checked = checkbox_values[1]
                self.check_box_3.checked = checkbox_values[2]
                self.check_box_4.checked = checkbox_values[3]

            if self.lapsed_lst:
                self.lapsed.text = self.lapsed_lst[-1]

            if self.default_lst:
                self.default.text = self.lapsed_lst[-1]

            if self.npa:
                self.npa.text = self.lapsed_lst[-1]

            if self.min_month_list:
                self.min_months.text = str(self.min_month_list[-1])

            if self.disc_coupans_list:
                if self.disc_coupans_list[-1] == "Yes":
                    self.radio_button_3.text = "Yes"
                    self.radio_button_4.text = "No"
                else:
                    self.radio_button_3.text = "No"
                    self.radio_button_4.text = "Yes"

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.dashboard.manage_products.view_product')
        selected_product_id = None

        if (
            selected_product_id is None
            or self.name.selected_value is None
            or self.product_category.selected_value is None
            # or self.drop_down_2.selected_value == ""
            # or self.text_box_3.text == ""
            # or self.text_box_4.text == ""
            # or self.intr_type is None
            # or self.max_amount.text == ""
            # or self.min_amount.text == ""
            # or self.min_tenure.text == ""
            # or self.max_tenure.text == ""
            # or self.roi.text == ""
        ):
            alert("Fill All Required Details")
        else:
            selected_row = self.product_data_grid.selected_row

            if selected_row is not None:
                selected_product_id = selected_row['product_id']
              
            data = app_tables.fin_product_details.get(product_id=selected_product_id)
            if data is None:
                alert("No Data Available Here")            
            else:
                data['product_group'] = self.name.selected_value
                data['product_name'] = self.product_name.text
                data['product_discription'] = self.text_area_1.text
                data['product_categories'] = self.product_category.selected_value
                data['processing_fee'] = int(self.text_box_3.text)
                data['extension_fee'] = int(self.text_box_4.text)
                data['membership_type'] = self.drop_down_2.selected_value
                data['interest_type'] = self.radio_button_1.text if self.radio_button_1.selected else self.radio_button_2.text
                data['min_amount'] = int(self.min_amount.text)
                data['max_amount'] = int(self.max_amount.text)
                data['min_tenure'] = int(self.min_tenure.text)
                data['max_tenure'] = int(self.max_tenure.text)
                data['roi'] = int(self.roi.text)
                data['foreclose_type'] = self.foreclose_type.selected_value
                data['foreclosure_fee'] = int(self.foreclosure_fee.text)
                data['emi_payment'] = self.checkbox_values
                data['extension_allowed'] = self.extension_allowed.selected_value
                data['lapsed_fee'] = int(self.lapsed.text)
                data['default_fee'] = int(self.default.text)
                data['npa'] = int(self.npa.text)
                data['min_months'] = int(self.min_months.text)
                data['discount_coupons'] = "Yes" if self.radio_button_3.selected else "No"

                Notification("Product details updated successfully").show()

    def button_1_copy_3_click(self, **event_args):
        open_form('admin.dashboard.manage_products.view_product')

    

