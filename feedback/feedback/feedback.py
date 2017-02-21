"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, Boolean, String 
from xblock.fragment import Fragment


class FeedbackXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )
    feedbackquestion = String(help="URL of the video page at the provider", default="How about the course", scope=Scope.content)
    answer = String(help="URL of the video page at the provider", default=None, scope=Scope.user_state)
    is_answered = Boolean(help="Has this student answered?", default=False,scope=Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the FeedbackXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/feedback.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/feedback.css"))
        frag.add_javascript(self.resource_string("static/js/src/feedback.js"))
        frag.initialize_js('FeedbackXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def post_answer(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        # assert data['hello'] == 'world'
        self.answer = data['answer']
        return {"answer": self.answer}

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        html_str = self.resource_string("static/html/feedback_edit.html")
        feedbackquestion = self.feedbackquestion or ''
        frag = Fragment(html_str.format(self=self))
        frag.add_javascript(self.resource_string("static/js/src/feedback_edit.js"))
        frag.initialize_js('FeedbackEditBlock')
        return frag


    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.feedbackquestion = data.get('feedbackquestion')

        return {'result': 'success'}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("FeedbackXBlock",
             """<feedback/>
             """),
            ("Multiple FeedbackXBlock",
             """<vertical_demo>
                <feedback/>
                <feedback/>
                <feedback/>
                </vertical_demo>
             """),
        ]
