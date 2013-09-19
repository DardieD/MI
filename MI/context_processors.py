'''
Custom Context Processors for MI
site_basics contains the site name, list of external links 
and other static links displayed throughout the templates 
(see templates/base.html)
'''

def site_basics(request):
        return {
            #Site Title for browser window as well as header
            'site_title':"Organization Name",
            #List of eternal links displayed in the header
            'site_links':[{'name':'Link 1','url':'#'},
            		  {'name':'Link 2','url':'#'},
            		  {'name':'Link 3','url':'#'}],
            #Link to logo image
            'logo':'MemberInterface/img/sample_logo.jpg',
            #Title for Welcome Message
            'welcome_title':'Welcome',
            #Body of Welcome Message
            'welcome_desc':'''
            		   This is sample content to be displayed on the welcome page. 
            		   It will contain some text that introduces the organization.
            		   '''
        }
