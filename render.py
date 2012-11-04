# Copyright 2012 Bogdan-Cristian Tataroiu

from xhpy.pylib import *

class :cs:page(:x:element):
    attribute str title @required
    children :cs:header, :cs:content, :cs:footer

    def render(self):
        css_files = [
            'static/css/bootstrap.min.css',
            'static/css/bootstrap-responsive.min.css'
        ]
        js_files = [
            'https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js',
            'static/js/bootstrap.min.js',
            'static/js/cs.js'
        ]

        # Compose head of page
        head = \
        <head>
            <title>{self.getAttribute('title')}</title>
            <style>{"""
                body {
                    padding-top: 50px;
                }

                .table .task-score {
                    text-align: center;
                }
            """}</style>
        </head>

        # Compose body of page
        body_container = \
        <div class="container">
            {self.getChildren('cs:content')}
            {self.getChildren('cs:footer')}
        </div>
        body = \
        <body>
            {self.getChildren('cs:header')}
            {body_container}
        </body>

        # Add CSS files to header
        for css_file in css_files:
            head.appendChild(
                <link href={css_file} rel="stylesheet" />)

        # Add JS files to end of body, so the pages load fast
        for js_file in js_files:
            body.appendChild(
                <script type="text/javascript" src={js_file} />)

        # Compose the page
        return \
        <x:doctype>
            <html>
                {head}
                {body}
            </html>
        </x:doctype>

class :cs:header(:x:element):
    def render(self):
        return \
        <div class="navbar navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">
                    <a class="brand" href="">
                        Cambridge ACM Eliminations 2012
                    </a>
                    <ul class="nav" id="navTabs">
                        <li class="active">
                            <a href="#problemset">
                                Problem Set
                            </a>
                        </li>
                        <li>
                            <a href="#rankings">
                                Rankings
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>


class :cs:content(:x:element):
    def render(self):
        return \
        <div class="main-content">
            {self.getChildren()}
        </div>


class :cs:footer(:x:element):
    def render(self):
        return \
        <x:frag>
            <hr />
            <footer class="footer">
                <p class="pull-right">
                    <a href="#">Back to top</a>
                </p>
                <p>
                    Copyright 2012{' '}
                    <a href="bct25@cam.ac.uk">Bogdan Tataroiu</a>{' '}and{' '}
                    <a href="ss958@cam.ac.uk">Szymon Sidor</a>.
                </p>
            </footer>
        </x:frag>


class :ui:tabbed-content(:x:element):
    attribute str active

    children :ui:tab-pane, :ui:tab-pane*

    def render(self):
        xhp = \
        <div class="tab-content">
        </div>

        for child in self.getChildren('ui:tab-pane'):
            child.setAttribute('active',
                child.getAttribute('name') == self.getAttribute('active'))
            xhp.appendChild(child)

        return xhp


class :ui:tab-pane(:x:element):
    attribute str name @required,
              bool active = False

    def render(self):
        class_ = 'tab-pane'
        if self.getAttribute('active'):
            class_ += ' active'
        return \
        <div class={class_} id={self.getAttribute('name')}>
            {self.getChildren()}
        </div>


class :footer(:xhpy:html-element):
    category %flow
    children (pcdata | %flow)*
    def __init__(self, attributes={}, children=[]):
        super(:xhpy:html-element, self).__init__(attributes, children)
        self.tagName = 'footer'


class :cs:task-list(:x:element):
    attribute list tasks @required
    def render(self):
        tbody = <tbody />
        table = \
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Task ID</th>
                    <th>Name</th>
                    <th>Solve Count</th>
                </tr>
            </thead>
            {tbody}
        </table>

        for task_id, task_name, solve_count in self.getAttribute('tasks'):
            task_url = 'http://acm.sgu.ru/problem.php?contest=0&problem=' + \
                task_id
            badge_class = 'badge'
            if solve_count >= 1:
                badge_class = 'badge badge-info'

            tbody.appendChild(
                <tr>
                    <td><a href={task_url}>{task_id}</a></td>
                    <td><a href={task_url}>{task_name}</a></td>
                    <td><span class={badge_class}>{solve_count}</span></td>
                </tr>)

        return table


class :cs:rankings(:x:element):
    attribute list tasks @required,
              list rankings @required

    def render(self):
        header_tasks = <x:frag />
        for task_id, task_name, solve_count in self.getAttribute('tasks'):
            task_url = 'http://acm.sgu.ru/problem.php?contest=0&problem=' + \
                task_id
            header_tasks.appendChild(
                <th class="task-score">
                    <a href={task_url} rel="tooltip" title={task_name}>
                        {task_id}
                    </a>
                </th>)

        tbody = <tbody />
        table = \
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Team</th>
                    {header_tasks}
                    <th>Score</th>
                    <th>Time penalty</th>
                </tr>
            </thead>
            {tbody}
        </table>

        for team in self.getAttribute('rankings'):
            task_scores = <x:frag />
            for task_score in team.get('tasks', []):
                if task_score.get('verdict') == None:
                    xhp = <span class="badge">-</span>
                elif task_score.get('verdict') == 'Accepted':
                    xhp = \
                    <x:frag>
                        <span class="badge badge-success">
                            {task_score.get('bombs', 0)}
                        </span>
                        <br />
                        {self.get_penalty_string(task_score.get('time'))}
                    </x:frag>
                else:
                    xhp = \
                    <span class="badge badge-important">
                        {task_score.get('bombs', 0)}
                    </span>
                task_scores.appendChild(<td class="task-score">{xhp}</td>)
            tbody.appendChild(
                <tr>
                    <td>{team.get('user', 'Error')}</td>
                    {task_scores}
                    <td>{team.get('score', 0)}</td>
                    <td>{int(team.get('total_time', 0))}</td>
                </tr>)

        return table

    def get_penalty_string(self, ts):
      ts = int(ts)
      if(ts<60):
        return "%ds" % (ts % 60)
      elif(ts<3600):
        return "%dm %ds" % (ts / 60, ts % 60)
      else:
        return "%dh %dm %ds" % (ts / 3600, (ts / 60)%60, ts % 60)
      

def render_acm(tasks, rankings):
    title = "Cambridge ACM Eliminations 2012"

    problem_set_pane = \
    <x:frag>
        <h2>Problem Set</h2>
        <cs:task-list tasks={tasks} />
    </x:frag>
    rankings_pane = \
    <x:frag>
        <h2>Rankings</h2>
        <cs:rankings tasks={tasks} rankings={rankings} />
    </x:frag>

    page = \
    <cs:page title={title}>
        <cs:header />
        <cs:content>
            <ui:tabbed-content active="problemset">
                <ui:tab-pane name="problemset">
                    {problem_set_pane}
                </ui:tab-pane>
                <ui:tab-pane name="rankings">
                    {rankings_pane}
                </ui:tab-pane>
            </ui:tabbed-content>
        </cs:content>
        <cs:footer />
    </cs:page>

    return str(page)
